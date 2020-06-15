from SaveMongoDB import SaveToDB
from Crawler import Crawler


##maincode



region_code = [1,3]#1:台北, 3:新北 
sex_code = [1,2,3]#1:男性, 2:女性, 3:男女皆可
shape_code = [1,2,3,4]#1:公寓, 2:電梯大樓, 3:透天厝, 4:別墅

for region in region_code:
    for sex in sex_code:
        for shape in shape_code:
            Records = Crawler(region,sex,shape) 
            SaveToDB(Records)

##  拆開用多線程去跑增加效率

# def main1():
#     sex = 1
#     for region in region_code:
#         for shape in shape_code:
#             Records = Crawler(region,sex,shape) 
#             SaveToDB(Records)

# ##
# def main2():
#     sex = 2
#     for region in region_code:
#         for shape in shape_code:
#             Records = Crawler(region,sex,shape) 
#             SaveToDB(Records)
# ##
# def main3():
#     sex = 3
#     region =1
#     for shape in shape_code:
#         Records = Crawler(region,sex,shape) 
#         SaveToDB(Records)

# def main4():
#     sex = 3
#     region =3
#     for shape in shape_code:
#         Records = Crawler(region,sex,shape) 
#         SaveToDB(Records)

# main4()