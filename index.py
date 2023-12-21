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


@app.route("/")
def index():
    homepage = "<br><a href=/pizza>pizza</a><br>"
    return homepage
@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]

    if intent_name == "your_intent_name":  # 替換成您 Dialogflow 意圖的名稱
        # 在這裡處理您的邏輯，可以調用之前定義的 pizza 函數

        response = {
            "fulfillmentText": "您的回應訊息"
        }

        return jsonify(response)

    else:
        return jsonify({"fulfillmentText": "未知的意圖"})
@app.route("/pizza", methods=["POST","GET"]) 
def pizza():
    if request.method == "POST":
        title = request.form["title"]
        info = ""
        db = firestore.client()     
        collection_ref = db.collection("Pizza").order_by("title")
        docs = collection_ref.get()
        for doc in docs:
            if title in doc.to_dict()["title"]: 
                info += "活動：" + str(doc.to_dict()["title"]) + "<br>" 
                info += "內容：" + doc.to_dict()["detail"] + "<br>"
                info += "連結：" +"<a href=" + doc.to_dict()["buyUrl"] +">" + doc.to_dict()["buyUrl"] +"<br>"          
        return info
    else:  
        return render_template("pizza.html")
app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    action =  req["queryResult"]["action"]
    if(action == "Pizza"):
        title = req["queryResult"]["parameters"]["title"]
        info = ""
        db = firestore.client()     
        collection_ref = db.collection("Pizza").order_by("title")
        docs = collection_ref.get()
        for doc in docs:
            if title in doc.to_dict()["title"]: 
                info += "活動：" + str(doc.to_dict()["title"]) + "<br>" 
                info += "內容：" + doc.to_dict()["detail"] + "<br>"
                info += "連結：" +"<a href=" + doc.to_dict()["buyUrl"] +">" + doc.to_dict()["buyUrl"] +"<br>"
    return make_response(jsonify({"fulfillmentText": info}))      


if __name__ == "__main__": 
    app.run(debug=True)
