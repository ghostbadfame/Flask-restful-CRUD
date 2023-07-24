from flask import Flask, render_template, request, redirect,jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_restful import Resource, Api , reqparse

app = Flask(__name__)
api=Api(app)
client = MongoClient('mongodb+srv://kapoorshivam77:shivam2002@cluster0.8oexlkc.mongodb.net/?retryWrites=true&w=majority')
db = client['CoRider']
collection = db['Users']
    

data_post_args = reqparse.RequestParser()
data_post_args.add_argument("name",type=str , help="Name is required",required = True)
data_post_args.add_argument("email",type=str , help="Email is required",required = True)
data_post_args.add_argument("password",type=str , help="Password is required",required = True)
# For securing the password we can use hashing

data_update_args = reqparse.RequestParser()
data_update_args.add_argument("name",type=str)
data_update_args.add_argument("email",type=str)
data_update_args.add_argument("password",type=str)

class dataIO(Resource):
    def get(self):
        allData = db['Users'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            name = data['name']
            email = data['email']
            dataDict = {
                'id':str(id),
                'name':name,
                'email':email
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)
    
    def post(self):
        args=data_post_args.parse_args()
        # print(args)
        _name=args["name"]
        _email=args["email"]
        _password=args["password"]
        db['Users'].insert_one({
                "name":_name,
                "email":_email,
                "password":_password
            })
        return jsonify({
                'status': 'Data is posted to MongoDB!',
                "name":_name,
                "email":_email,
                "password":_password
            })
    
class databyId(Resource):
    def get(self,id):
        if request.method == 'GET':
            data = db['Users'].find_one({'_id': ObjectId(id)})
            id = data['_id']
            name = data['name']
            email = data['email']
            dataDict = {
                'id':str(id),
                'name':name,
                'email':email
            }
            print(dataDict)
            return jsonify(dataDict)
    
    def put(self,id):
        args=data_update_args.parse_args()
        _name=args["name"]
        _email=args["email"]
        _password=args["password"]
        db['Users'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "name":_name,
                    "email":_email,
                    "password":_password
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})
    
    def delete(self,id):    
        db['Users'].delete_many({'_id': ObjectId(id)})
        print('\n # Deleted # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})


api.add_resource(dataIO,'/manipulate') 
api.add_resource(databyId,'/crud/<string:id>')


if __name__ == '__main__':
    app.debug = True
    app.run()



