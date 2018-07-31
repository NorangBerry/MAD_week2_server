from flask import Flask, request, render_template, jsonify,send_file
from pymongo import MongoClient
import pymongo
from time import gmtime,strftime
from bson import ObjectId
import json
app = Flask(__name__)
@app.route('/')
def main():
    print("connected")
    return "root"


@app.route('/check-image/<user_id>', methods=['GET'])
def check_image(user_id):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.users
    user = collection.find_one({"id":user_id})
    image = user['image']
    image_name = image['image_name']
    print(image_name)
    if(image_name == ""):
        return send_file('1531344752806.png', mimetype='image/png')
    else:
        return send_file(image_name, mimetype='image/png')

@app.route('/login/<user_id>',methods=['GET'])
def hello_user(user_id):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.users
    password = request.args.get('password')
    item = collection.find_one({"id":user_id})
    print(item['password'])
    if(item is None):
        return "false"
    if(item['password']==password):
        return "true"
    else:
        return "false"
@app.route('/users',methods={'GET'})
def show_users():
    client = MongoClient('mongodb://127.0.0.1:27107')
    db = client.week2db
    collection = db.users
    query = collection.find()
    user_list = "user start\n"
    for user in query:
        print(user)
    return user_list
@app.route('/uu',methods={'GET'})
def get_uu():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.users
    query = collection.find().sort('id',1)
    item_list = ""
    for item in query:
        item_list = item_list+item['id']+'!!'+item['status']+'/'
    return item_list
@app.route('/regist_user')
def regist_user():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.users
    db.users.insert({"id":request.args.get("id"),"password":request.args.get("password"),"status":"null", "image":{"image_name":"", "image_path":""}})
    return ''
@app.route('/board',methods={'GET'})
def show_board():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.posts
    query = collection.find()
    item_list = ""
    for item in query:
        item_list = item_list+str(item['_id'])+'\t'+item['title']+'\t'+item['uploader']+'\t'+item['time']+'/'
    return str(item_list)
#    return item_list
@app.route('/board/<title>',methods={'GET'})
def show_post_title(title):
    return title
@app.route('/post/<post_id>')
def show_post(post_id):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.posts
    print(post_id)
    post = collection.find_one({"_id":ObjectId(post_id)})
    post_info = "**line seperate**\n"+post['title']+'\n'+post['uploader']+'\n'+post['time']+'\n'+post['content']+'\n'
    image_list = post['images']
    for image in image_list:
        post_info = post_info +"**image seperate**\n" + image['image_name'] + '\n'
    return post_info
@app.route('/post_delete')
def del_post():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.posts
    print(request.args.get('_id'))
    uploader = collection.find_one({'_id':ObjectId(request.args.get('_id'))})
    uploader = uploader.get('uploader')
    print(uploader)
    if(uploader != request.args.get('user')):
        return "fail"
    collection.delete_one({'_id':ObjectId(request.args.get('_id'))})
    return "delete"
@app.route('/post/images/<image_name>',methods=['POST',"GET"])
def get_image(image_name):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.posts
    return send_file(image_name.replace('*','/'),mimetype='image/png')

@app.route('/add-post',methods=['GET','POST'])
def savePost():
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    post = {"title" : request.form.get("title"),"uploader":request.form.get("uploader"),"time":now, "content" : request.form.get("content"),"images":[]}
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.posts
    image_list=[]
    size=request.form.get("size")
    for i in range(int(size)):
        image = request.files.get("image"+str(i))
        image_name = "posts/"+image.filename
        image.save(image_name)
        small_img = Image.open(image_name)
        size = 128,128
        small_img.thumbnail(size)
        small_img.save("posts/small/"+image.filename)
        image_list.append({"image_name":image_name})
    post["images"]=image_list
    _id = collection.insert(post)
    return str(_id)
       # print("fail to save post")
      #  return "empty"
@app.route('/imagenames',methods=['POST','GET'])
def get_image_names():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.posts
    query = collection.find()
    image_list = ""
    for item in query:
        if item['images']!=[]:
            image_list = "**id seperate**\n"+str(item['_id'])+'\n'+item['uploader']+'\n'
            for image_name in item['images']:
                image_list = image_list+"**image seperate**\n"+"posts/small/"+image_name['image_name'].replace('posts/','')+"\n"
    return image_list
import base64
@app.route('/images',methods=['POST','GET'])
def ret_images():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.posts
    query = collection.find()
    index = request.args.get('index')
#    line_seperator = "**line seperator**"
#    for item in query:
#        _id = item['_id']
#        item_images = item['images']
    #    for item_image in item_images:
    #        filename = item_image['image_name']
    for i in query:
        print(i.get('image_name'))
        return send_file(i.get('image_name'),mimetype='image/png')
    return 'x'

@app.route('/profile-image/<id_>')
def retImage(id_):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.users
    query = collection.find_one({"id":id_})
    image = query['image']
    image_name = image['image_name']
    print(image_name+"check")
    return send_file(image_name, mimetype='image/png')

@app.route('/update-profile')
def updateProfile():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.users
    status = request.args.get('status')
    print(status)
    try:
        collection.update({"id":request.args.get('id')},
            {'$set': {"status" : status}})
    except:
        print("fail update profile")
    return "end"


from PIL import Image
import io
@app.route('/add-image',methods=['GET','POST'])
def saveImages():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.posts
    query = collection.find({"_id":ObjectId(request.args.get('id'))})
    image = request.files.get('image')
    image_name = image.filename
    image.save(image_name)

    try:
        collection.update({"_id":ObjectId(request.args.get('id'))},
            {'$push': {
                "images":{
                    "image_name":image_name,
                    "image_path":image_name+".png"
                    }
                }
            }
        )
    except:
        print("fail upload image")
    return "end"

@app.route('/update-profile-image',methods=['GET', 'POST'])
def saveImage():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.users
    image = request.files.get('image')
    image_name = image.filename
    print(image_name)
    image.save(image_name)
    collection.update({"id":request.form.get('id')},
            {'$set': {
                "image":{
                    "image_name":image_name,
                    "image_path":image_name+".png"
                    }
                }
            }
        )
    return "end"

@app.route('/init-profile')
def initImage():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.week2db
    collection = db.users
    try:
        collection.update({"id":request.args.get('id')},
                {'$set': {
                    "image":{
                        "image_name":"",
                        "image_path":""
                        }
                    }
                }
            )
    except:
        print("fail initiate image")
    return "end"
if __name__=='__main__':
    app.run('0.0.0.0',8080)
