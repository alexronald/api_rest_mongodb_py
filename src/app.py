
from flask import Flask, Response, jsonify, request 
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/python_mongodb'
mongo = PyMongo(app)

@app.route('/users',methods=['POST'])
def Create_user():
    user_name = request.json['user_name']
    email = request.json['email']
    password = request.json['password']

    if user_name and email and password:
        password_hash = generate_password_hash(password)
        id = mongo.db.users.insert_one(
            {'username':user_name, 'email':email, 'password':password_hash}
            )
        response ={ 'id':str(id), 'username':user_name, 'email':email, 'password': password_hash}
        return response
    else:
        return not_found()
    
@app.route('/users', methods=['GET'])
def get_users():
    users=mongo.db.users.find()
    response=json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id':ObjectId(id)})
    response = jsonify({'massage': 'user '+ id + 'delete successfully'})
    return response

@app.route('/users/<id>',methods=['PUT'])
def update_user(id):
    new_user_name = request.json['user_name']
    new_email = request.json['email']
    new_password = request.json["password"]

    if new_user_name and new_password and new_email:
        password_hash= generate_password_hash(new_password)
        user = mongo.db.users.update_one({'_id':ObjectId(id)},{'$set':{
            'user_name':new_user_name,
            'email':new_email,
            'password':password_hash
        }})
        response = jsonify({'message':'user '+id+' was update successfully'})
        return response


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify(
        {'message':' resource not found: '+ request.url, ' status ':404}
    )
    response.status_code = 404
    return response



if __name__ == '__main__':
    app.run(debug=True)