import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)



import requests
from bs4 import BeautifulSoup
url = "https://www.pizzahut.com.tw/menu/?fms=nav&parent_id=263"
Data = requests.get(url)
Data.encoding = "utf-8"

db = firestore.client()
sp = BeautifulSoup(Data.text, "html.parser")
result=sp.select(".pdpop-li")

info = ""
for item in result:
  pic = item.find("img").get("data-original").replace(" ", "")
  name = item.find(class_="pdpop-name").text
  price = item.find(class_="pdpop-price").find("span").text
  doc = {
      "name": name,
      "pic": pic,
      "price": price
    }


 
  doc_ref = db.collection("產品介紹").add(doc)
  #doc_ref.set(doc)