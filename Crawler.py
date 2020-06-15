import pandas as pd 
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time        
import requests as req
import json

from SaveMongoDB import SaveToDB

def Crawler(Region, Sex, Shape):


    url ='https://rent.591.com.tw/?kind=0&region=' + str(Region) + '&sex=' + str(Sex) + '&shape=' + str(Shape) 
    rs = req.session()
    print(url)
    ####STEP 0 爆改Cookies####
    res = rs.get(url)
    
    print(res.headers)
    rs.cookies.set('urlJumpIp', str(Region))  # <- 縣市
    res = rs.get(url)

    ####STEP 1 取得Token#####

    for_token_main_page = bs(res.text, 'html.parser')
    t = for_token_main_page.find('span',class_='TotalRecord')
    if t == None:
        return 0
    else :
    
        total = int(for_token_main_page.find('span',class_='TotalRecord').text.split(' ')[1])
    print(total)
    token = for_token_main_page.find(attrs={"name":"csrf-token"})['content']
    print(res.headers)

    ####STEP 2 設定Headers#####
    headers = {
        'X-CSRF-TOKEN': token,
        'X-Requested-With': 'XMLHttpRequest'

    }

    ####STEP 3 針對個別性別及縣市做設定#####
    totalRows = int(total) //30+1
    firstRow = 0
    DataFrameAllList = []
    for firstRow in range(totalRows):
        print(totalRows , firstRow)
        apiurl = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=' + str(Region) + '&sex=' + str(Sex) + '&shape=' + str(Shape) + '&firstRow='+ str(firstRow*30) + '&totalRows=' + str(total)
        #apiurl = link + '&firstRow=' + str(firstRow*30) + '&totalRows=' + total
        data = rs.get(apiurl,headers = headers)
        jsondata = data.json()
        df_thisrow = pd.DataFrame(jsondata['data']['data'])
        DataFrameAllList.append(df_thisrow)


    df_all = pd.concat(DataFrameAllList)
    df_all = df_all.drop(['user_id', 'address', 'type', 'post_id', 'regionid', 'sectionid',
        'streetid', 'room', 'area', 'storeprice', 'comment_total',
        'comment_unread', 'comment_ltime', 'hasimg', 'kind', 'shape',
        'houseage', 'posttime', 'updatetime', 'refreshtime', 'checkstatus',
        'status', 'closed', 'living', 'condition', 'isvip', 'mvip',
        'is_combine', 'cover', 'browsenum', 'browsenum_all', 'floor2', 'floor',
            'cases_id', 'social_house', 'distance', 'search_name',
        'mainarea', 'balcony_area', 'groundarea', 'housetype',
            'alley_name', 'lane_name', 'addr_number_name',
            'address_img', 'cases_name',  'layout_str',
        'allfloor', 'house_img', 'houseimg', 'cartplace',
        'space_type_str', 'photo_alt', 'addition4', 'addition2', 'addition3',
        'vipimg', 'vipstyle', 'vipBorder', 'new_list_comment_total',
        'comment_class', 'price_hide',  'photoNum', 'filename',
            'new_img', 'regionname', 'sectionname', 'icon_name',
        'icon_class', 'fulladdress', 'address_img_title', 'browsenum_name',
        'unit',  'addInfo', 'layout', 'houseid',
        'onepxImg' , 'kind_name_img'] , axis=1)

    df_all["type"] = df_all["nick_name"].apply(lambda x : x.split(' ')[0])
    df_all = df_all.drop(["nick_name"], axis=1)


    ####STEP 4 爬取電話號碼#####
    phone_num_list = []
    id_list = df_all['id'].tolist()

    for _id in id_list:

        detail_page = req.get('https://rent.591.com.tw/rent-detail-' + str(_id) + '.html')
        detail_page = bs(detail_page.text, 'html.parser')
        
        try:
            ph_num = str(detail_page.find('span',class_='dialPhoneNum')).split('"')[-2]
            phone_num_list.append(ph_num)
        except:
            phone_num_list.append('Null')
    phoneDF = pd.DataFrame(phone_num_list)
    df_all["PhoneNum"] = phoneDF

    ####STEP 5 加上性別資料####
    if Sex == 3:
        df_all["Sex"] = "皆可"
    elif Sex == 2:
        df_all["Sex"] = "女"
    elif Sex == 1:
        df_all["Sex"] = "男"

    if Shape == 3:
        df_all["Shape"] = "透天厝"
    elif Shape == 2:
        df_all["Shape"] = "電梯大樓"
    elif Shape == 1:
        df_all["Shape"] = "公寓"
    elif Shape == 4:
        df_all["Shape"] = "別墅"

    

    ####STEP 6 DataFrame轉回Dict####
    records = df_all.to_dict('records')

    return records

