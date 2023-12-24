import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
url = "https://www.pizzahut.com.tw/promotions/?fms=nav&parent_id=2750"
Data = requests.get(url)
Data.encoding="utf-8"
#print(Data.text)

# 初始化 Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


sp = BeautifulSoup(Data.text, "html.parser")
result=sp.select(".promotion_list_item")
info=""
url = sp.select(".img[data-original]")
for element in url:
    print(
        "https://welovekai.com/proxy.php?link="
        + element["data-original"].replace("\n", "").replace("\r", "")
    )

for x in result:
    test = x
    price = x.find("span",class_="pro-li-name").text
    detail = x.find("p",class_="pro-list-desc").text
    # buyUrl = "https://www.pizzahut.com.tw/" + x.find("a").get('href') 

    photo = x.find("img").get("data-original")
    buyUrl='https://www.pizzahut.com.tw/' + x.find("a").get('href')
    # hyperlink = 'https:' + x.find('img').get('href')
    info += price+"\n"+detail+"\n\n"
    docs = {
        'detail': detail,
        'photo': photo,
        'title': price, 
        'buyUrl': buyUrl
    }
    doc_ref = db.collection("優惠推薦").add(docs)