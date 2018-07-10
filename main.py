from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
import pymongo
from bson import ObjectId
import json
app = Flask(__name__)
@app.route('/')
def main():
    print("connected")
    return "root"
#@app.route('/image/<imagename>',methods=['GET'])
#def saveImage(imagename):
#    image = {"name" : imagename, "image" : request.stream.read()}
#    client = MongoClient('mongodb://127.0.0.1:27017')
#    db = client.week2db
#    collection = db.images
#    try:
#        collection.insert(image)
#    except:
#        print("fail")
#    print(request.stream.read())
#    return "yourData:"+imagename



@app.route('/login/<user_id>',methods=['GET'])
def hello_user(user_id):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.users
    password = request.stream.read().decode('utf-8')
    print(password)
    if(collection.find({"id":user_id}).count()!=0):
        return "find"
    else:
        collection.insert({"id":user_id,"password":password})
        return "add"

@app.route('/users',methods={'GET'})
def show_users():
    client = MongoClient('mongodb://127.0.0.1:27107')
    db = client.week2db
    collection = db.users
    query = collection.find()
    user_list = "user start\n"
    for user in query:
        print(user)
       # user_list=user_list+user['id']+'\n'
    return user_list
@app.route('/uu',methods={'GET'})
def get_uu():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.users
    query = collection.find().sort('id',1)
    item_list = ""
    for item in query:
        item_list = item_list+item['id']+'!!!'
    return item_list

@app.route('/board',methods={'GET'})
def show_board():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.posts
    query = collection.find()
    item_list = ""
    for item in query:
        item_list = item_list+item['title']+'\t'+item['uploader']+'\t'+item['time']+'/'
    print(item_list)
    print(type(item_list))
    return str(item_list)
#    return item_list
@app.route('/board/<title>',methods={'GET'})
def show_post(title):
    return title

@app.route('/add-post',methods=['GET'])
def savePost():
    post = {"title" : request.args.get("title"),"uploader":"temp","time":"temp", "content" : request.stream.read().decode('utf-8'),"images":[{"image_name":'aa'}]}
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.posts
    try:
        _id = collection.insert(post)
        return str(_id)
    except:
        print("fail to save post")
        print(request.stream.read())
        return "empty"
@app.route('/add-image')
def saveImage():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.posts
    print(ObjectId(request.args.get('id')))
    query = collection.find({"_id":ObjectId(request.args.get('id'))})
    for item in query:
        print(item['title'])
    image_name = request.args.get('name')
    image = request.stream.read()
    try:
        collection.update({"_id":ObjectId(request.args.get('id'))},
            {'$push': {
                "images":{
                    "image_name":image_name,
                    "image":image
                    }
                }
            }
        )
    except:
        print("fail upload image")
    return "end"
if __name__=='__main__':
    app.run('0.0.0.0',8080)
