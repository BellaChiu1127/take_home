import os
import pandas as pd 
path = './input/'
filelist = os.listdir(path)


def CreateDataframe(data):
    data_readcsv = pd.read_csv(data)
    data_dataframe = pd.DataFrame(data_readcsv)
    data_dataframe = data_dataframe.drop(0 , axis=0)
    return data_dataframe


for file in filelist:        
    if file[0] == 'a':
        df_a = CreateDataframe(path + file)
    elif file[0] == 'b':
        df_b = CreateDataframe(path + file)
    elif file[0] == 'e':
        df_e = CreateDataframe(path + file)       
    elif file[0] == 'f':
        df_f = CreateDataframe(path + file)
    elif file[0] == 'h':
        df_h = CreateDataframe(path + file)

df_all = pd.concat([df_a, df_b, df_e, df_f, df_h])


####Fliter_A Start####


df_all["Type"] =  df_all["建物型態"].apply(lambda x : str(x)[0:4])
df_all["Floor"] = df_all["總樓層數"].apply(lambda x : len(str(x)) )


mask_usage = df_all["主要用途"] == '住家用' 
mask_type = df_all["Type"] == '住宅大樓'
mask_floor = df_all["Floor"] >= 3  
mask_floor_11 = df_all["總樓層數"] != "十一層" 
mask_floor_12 = df_all["總樓層數"] != "十二層"

df_all = df_all.drop(["Type","Floor"],axis = 1)
Fliter_A = df_all[(mask_usage & mask_type & mask_floor & mask_floor_11 & mask_floor_12)]
Fliter_A.to_csv('./output/Fliter_A.csv', index=False)

####Fliter_A End#####

####Fliter_B Start#####

all_count = df_all.shape[0]  ###Row數作為總筆數

df_all["Garage"] = df_all["交易筆棟數"].apply(lambda x : str(x)[-1])
df_all["Garage"] = df_all["Garage"].apply(lambda x : int(x))
Garage = df_all["Garage"].sum() 

##車位數都位於最後一個字元，取得最後一個字元轉數字後summary

df_all["總價元"] = df_all["總價元"].apply(lambda x : int(x))
AVG_HousePrice= df_all["總價元"].mean()  #房屋平均總價元

df_all["車位總價元"] = df_all["車位總價元"].apply(lambda x : int(x))
AVG_GaragePrice = df_all["車位總價元"].mean() ##車位平均總價元

col = ['總件數','總車位數','平均總價元','平均車位總價元']
data = [[all_count,Garage,AVG_HousePrice,AVG_GaragePrice]]
Fliter_B = pd.DataFrame(columns=col, data=data)
Fliter_B.to_csv('./output/Fliter_B.csv', index=False )


####Fliter_B End#####