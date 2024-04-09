from flask import Flask, request,jsonify
from bson import ObjectId
from flask_pymongo import PyMongo,ObjectId
from flask_cors import CORS


app=Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/python-react'
mongo=PyMongo(app)

CORS(app)

db=mongo.db.users

@app.route('/users', methods=['POST'])
def createUser():
    user_data = request.json
    result = db.insert_one({
        'name': user_data['name'],
        'email': user_data['email'],
        'password': user_data['password'],
    })
    user_id = result.inserted_id
    
    return jsonify(str(ObjectId(user_id)))

@app.route('/users', methods=['GET'])
def getUsers():
    users=[]
    db.find()
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name':doc['name'],
            'email':doc['email'],
            'password':doc['password']
        })
    return users

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user=db.find_one({'_id':ObjectId(id)})
    print(user)
    return jsonify({
        '_id':str(ObjectId(user['_id'])),
        'name':user['name'],
        'email':user['email'],
        'password':user['password']
    })
    

@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id):
    db.delete_one({'_id':ObjectId(id)})
    return jsonify({'msg':'Usuario eliminado'})

@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
    user_data = request.json
    db.update_one({'_id':ObjectId(id)},{'$set':{
        'name': user_data['name'],
        'email': user_data['email'],
        'password': user_data['password'],
    }})
    return 'Usuario actualizado'


if __name__ == "__main__":
    app.run(debug=True)

