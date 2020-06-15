import pymongo 

###DB連線設定###
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["591"]
mytable = mydb["Housessss"]


def SaveToDB (Records):
    if Records != 0:
        mytable.insert_many(Records)