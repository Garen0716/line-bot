import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


import requests
from bs4 import BeautifulSoup
url = "https://www.pizzahut.com.tw/pizza-news/?fms=nav&parent_id=2668"
Data = requests.get(url)
Data.encoding = "utf-8"
sp = BeautifulSoup(Data.text, "html.parser")
result=sp.select(".promotion_list_item")
db = firestore.client()
info = ""
for item in result:
  news = item.find(class_="pro-li-name").text
  pic = item.find("img").get("data-original").replace(" ", "")
  detail = item.find(class_="pro-list-desc").text
  info += news + "\n" + pic + "\n"+ detail + "\n"
  doc = {
      "news": news,
      "detail": detail,
      "pic": pic,
   }
  doc_ref = db.collection("新品嘗鮮").add(doc)
