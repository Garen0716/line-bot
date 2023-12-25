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


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    action =  req["queryResult"]["action"]
    if(action == "activity"):
        title = req["queryResult"]["parameters"]["title"]
        info = ""
        found=False
        db = firestore.client()     
        collection_ref = db.collection("活動").order_by("title")
        docs = collection_ref.get()
        for doc in docs:
            if title in doc.to_dict()["title"]:
                found = True    
                info += "活動：" + str(doc.to_dict()["title"]) + "\n"
                info += "內容：" + doc.to_dict()["detail"]+ "\n" 
                info += "圖片：" + doc.to_dict()["photo"]+ "\n" 
                info += "連結：" + doc.to_dict()["buyUrl"]+ "\n"
                return make_response(jsonify({"fulfillmentText": info}))
        if found:
            info = "找不到您搜尋的活動"
            return make_response(jsonify({"fulfillmentText": info}))
    elif (action=="product"):
        title = req["queryResult"]["parameters"]["name"]
        info = ""
        found=False
        db = firestore.client()     
        collection_ref = db.collection("產品介紹").order_by("name")
        docs = collection_ref.get()
        for doc in docs:
            if title in doc.to_dict()["name"]:
                found = True    
                info += "產品：" + str(doc.to_dict()["name"]) + "\n" 
                info += "價格：" + doc.to_dict()["price"] + "\n"
                info += "圖片：" + doc.to_dict()["pic"] +"\n"
                return make_response(jsonify({"fulfillmentText": info}))
        if found:
            info = "找不到您搜尋的產品"
            return make_response(jsonify({"fulfillmentText": info}))
    elif (action=="news"):
        title = req["queryResult"]["parameters"]["news"]
        info = ""
        db = firestore.client()    
        found=False 
        collection_ref = db.collection("新品嘗鮮").order_by("news")
        docs = collection_ref.get()
        for doc in docs:
            if title in doc.to_dict()["news"]:
                found=True
                info += "產品：" + str(doc.to_dict()["news"]) + "\n" 
                info += "內容：" + doc.to_dict()["detail"] + "\n"
                info += "圖片：" + doc.to_dict()["pic"] +"\n"
                return make_response(jsonify({"fulfillmentText": info}))   
        if found:
            info = "找不到您搜尋的產品"
            return make_response(jsonify({"fulfillmentText": info}))            
if __name__ == "__main__": 
    app.run(debug=True)
