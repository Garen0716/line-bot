# import requests
# from bs4 import BeautifulSoup
# import firebase_admin
# from firebase_admin import credentials, firestore
# url = "https://www.pizzahut.com.tw/promotions/?fms=nav&parent_id=2750"
# Data = requests.get(url)
# Data.encoding="utf-8"
# #print(Data.text)

# # 初始化 Firebase
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

# db = firestore.client()


# sp = BeautifulSoup(Data.text, "html.parser")
# result=sp.select(class_=".content_list_wrap list-getFavDone")
# info=""

# for x in result:
#     title = x
#     price = x.find("div",class_="pro-li-name").text
#     detail = x.find("p",class_="pro-list-desc").text
#     # info += price+"\n"+detail+"\n\n"
#     Message = {
#             "price": price,
#             "detail": detail
#     }

#     # doc_ref = db.collection("Pizza").document(title)
#     # doc_ref.set(Message)
#     print(price)


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

    photo = x.find("img").get("src").replace(" ", "")
    buyUrl='https://www.pizzahut.com.tw/' + x.find("a").get('href')
    # hyperlink = 'https:' + x.find('img').get('href')
    info += price+"\n"+detail+"\n\n"
    docs = {
        'title': price, 
        'detail': detail,
        'buyUrl': buyUrl
        # 'buyUrl': buyUrl,
    }
    doc_ref = db.collection("Pizza").add(docs)