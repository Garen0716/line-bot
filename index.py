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
@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    action =  req["queryResult"]["action"]
    if(action == "activity"):
        title = req["queryResult"]["parameters"]["title"]
        info = ""
        found=False
        db = firestore.client()     
        collection_ref = db.collection("PIZZA").order_by("title")
        docs = collection_ref.get()
        for doc in docs:
            if title in doc.to_dict()["title"]:
                found = True    
                info += "活動：" + str(doc.to_dict()["title"]) 
                info += "內容：" + doc.to_dict()["detail"]+ "\n" 
                info += "圖片：" + doc.to_dict()["photo"] 
                info += "連結：" + doc.to_dict()["buyUrl"] 
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
                info += "圖片：" +"<a href=" + doc.to_dict()["pic"] +">" + doc.to_dict()["pic"] +"<br>"
                return make_response(jsonify({"fulfillmentText": info}))
        if found:
            info = "找不到您搜尋的產品"
            return make_response(jsonify({"fulfillmentText": info}))
    elif (action=="news"):
        title = req["queryResult"]["parameters"]["name"]
        info = ""
        db = firestore.client()    
        found=False 
        collection_ref = db.collection("新品嘗鮮").order_by("name")
        docs = collection_ref.get()
        for doc in docs:
            if title in doc.to_dict()["name"]:
                found=True
                info += "產品：" + str(doc.to_dict()["name"]) + "\n" 
                info += "價格：" + doc.to_dict()["detail"] + "\n"
                info += "圖片：" +"<a href=" + doc.to_dict()["pic"] +">" + doc.to_dict()["pic"] +"<br>"
            return make_response(jsonify({"fulfillmentText": info}))   
    if found:
            info = "找不到您搜尋的產品"
            return make_response(jsonify({"fulfillmentText": info}))    
         
    
        
        



if __name__ == "__main__": 
    app.run(debug=True)
