from flask import Flask, jsonify, request
from flask_pymongo import PyMongo



app = Flask(__name__)
###Flask2db連線設定###
app.config['MONGO_DBNAME'] = '591'
app.config['MONGO_URI'] = "mongodb://localhost:27017/591"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)
goods = mongo.db.Housessss

####- 【男生可承租】且【位於新北】的租屋物件
@app.route('/1', methods=['GET'])
def GetSearch1():
  output = []
  for s in goods.find({'Sex':'男', 'region_name': '新北市'}):    
    output.append({"id":s['id'] , 
                  "聯絡人":s['linkman'] , 
                  "聯絡人身份":s['type'] , 
                  "電話號碼":s['PhoneNum'] , 
                  "地址": s['region_name'] +s['section_name']+s['street_name'] , 
                  "樓層": s['floorInfo'], 
                  "價格": s['price'], 
                  "出租類型": s['kind_name'] ,
                  "房屋型態": s['Shape'],
                  "性別限制": s['Sex'] ,
                  "資料時間" : s['ltime']})


  return jsonify({'result_1' : output})

####- 以【聯絡電話】查詢租屋物件
@app.route('/2', methods=['GET'])
def GetSearch2():
  output = []
  for s in goods.find({'phone_num':'此處請以String格式輸入，如：0916-484-605'}):    
    output.append({"id":s['id'] , 
                  "聯絡人":s['linkman'] , 
                  "聯絡人身份":s['type'] , 
                  "電話號碼":s['PhoneNum'] , 
                  "地址": s['region_name'] +s['section_name']+s['street_name'] , 
                  "樓層": s['floorInfo'], 
                  "價格": s['price'], 
                  "出租類型": s['kind_name'] ,
                  "房屋型態": s['Shape'],
                  "性別限制": s['Sex'] ,
                  "資料時間" : s['ltime']})

  return jsonify({'result_2' : output})

####- 所有【非屋主自行刊登】的租屋物件
@app.route('/3', methods=['GET'])
def GetSearch3():
  output = []
  for s in goods.find({'type': { '$ne' : "屋主"} }):    
    output.append({"id":s['id'] , 
                  "聯絡人":s['linkman'] , 
                  "聯絡人身份":s['type'] , 
                  "電話號碼":s['PhoneNum'] , 
                  "地址": s['region_name'] +s['section_name']+s['street_name'] , 
                  "樓層": s['floorInfo'], 
                  "價格": s['price'], 
                  "出租類型": s['kind_name'] ,
                  "房屋型態": s['Shape'],
                  "性別限制": s['Sex'] ,
                  "資料時間" : s['ltime']})

  return jsonify({'result_3' : output})

####- 【臺北】【屋主為女性】【姓氏為吳】所刊登的所有租屋物件
@app.route('/4', methods=['GET'])
def GetSearch4():
  output = []
  for s in goods.find({ 'region_name':'台北市','type':'屋主'}):    
    if s["linkman"] == "吳小姐" or s["linkman"] == "吳女士" or s["linkman"] == "吳阿姨" or s["linkman"] == "吳太太" or s["linkman"] == "吳媽媽" or s["linkman"] == "吳Ms":
      output.append({"id":s['id'] , 
                    "聯絡人":s['linkman'] , 
                    "聯絡人身份":s['type'] , 
                    "電話號碼":s['PhoneNum'] , 
                    "地址": s['region_name'] +s['section_name']+s['street_name'] , 
                    "樓層": s['floorInfo'], 
                    "價格": s['price'], 
                    "出租類型": s['kind_name'] ,
                    "房屋型態": s['Shape'],
                    "性別限制": s['Sex'] ,
                    "資料時間" : s['ltime']})

  return jsonify({'result_4' : output})


if __name__ == '__main__':
  app.run(debug=True,port=8000)