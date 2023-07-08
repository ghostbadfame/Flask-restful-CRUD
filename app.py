from flask import Flask, render_template, request, redirect,jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb+srv://kapoorshivam77:shivam2002@cluster0.8oexlkc.mongodb.net/?retryWrites=true&w=majority')
db = client['CoRider']
collection = db['Users']

@app.route('/create', methods=['POST'])
def create():
    
    _json = request.json 
    _name= _json["name"]
    _email= _json['email']
    _password=_json['password']

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

@app.route('/getAll', methods=['GET'])
def find():
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
        
    

# GET a specific data by id
@app.route('/getOne/<string:id>', methods=['GET'])
def findOne(id):
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
        
# DELETE a data
@app.route('/deleteData/<string:id>', methods=['DELETE'])
def deletebyId(id):    
    if request.method == 'DELETE':
        db['Users'].delete_many({'_id': ObjectId(id)})
        print('\n # Deleted # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

# UPDATE a data by id 
@app.route('/updateData/<string:id>', methods=['PUT'])
def updatebyId(id):       
    if request.method == 'PUT':
        _json = request.json 
        _name= _json["name"]
        _email= _json['email']
        _password=_json['password']

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

if __name__ == '__main__':
    app.debug = True
    app.run()



