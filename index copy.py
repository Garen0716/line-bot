from flask import Flask, render_template, request,make_response,jsonify
from datetime import datetime, timezone, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
import requests 
from bs4 import BeautifulSoup 

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
app = Flask(__name__)
db = firestore.client()


    
# action = "Hot拼盤樂享餐 / $1288"
# if(action == action):
#         info = ""
#         db = firestore.client()     
#         collection_ref = db.collection("Pizza").order_by("detail").get()
#         docs = collection_ref
#         print(collection_ref.get())
#         for doc in docs:
#             if action in doc.to_dict()["title"]: 
#                 info += "活動：" + str(doc.to_dict()["title"]) + "<br>" 
#                 info += "內容：" + doc.to_dict()["detail"] + "<br>"
#                 info += "連結：" +"<a href=" + doc.to_dict()["buyUrl"] +">" + doc.to_dict()["buyUrl"] +"<br>"
#         print(info)
# print(info)                  

action = "Hot拼盤樂享餐 / $1288"
info = ""

if action:
    db = firestore.client()     
    collection_ref = db.collection("PIZZA").order_by("title")
    docs = collection_ref.get()

    for doc in docs:
        if action in doc.to_dict()["title"]:
            info += "活動：" + str(doc.to_dict()["title"]) + "<br>" 
            info += "內容：" + doc.to_dict()["detail"] + "<br>"
            info += "連結：" + "<a href=" + doc.to_dict()["buyUrl"] + ">" + doc.to_dict()["buyUrl"] + "<br>"

    print(info)

# if __name__ == "__main__": 
#     app.run(debug=True)
