import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from dotenv import load_dotenv, dotenv_values

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI']=os.getenv("MONGODB_URI")
mongo = PyMongo(app)
db = mongo.db

CORS(app)

@app.route('/tools', methods=['GET'])
def get_tools():
     tools = []
     for doc in db.tools.find():
          tools.append({
               '_id': str(ObjectId(doc['_id'])),
               'name': doc['name'],
               'description': doc['description'],
               'url': doc['url']
          })
     return jsonify(tools)

@app.route('/tools', methods=['POST'])
def add_tool():
     new_tool = db.tools.insert_one({
          'name': request.json['name'],
          'description': request.json['description'],
          'url': request.json['url']
     })

     return jsonify({'id': str(new_tool.inserted_id), 'msg': 'Tool successfully added'})

@app.route('/tools/<id>', methods=['GET'])
def get_tool(id):
     user = db.tools.find_one({'_id': ObjectId(id)})

     return jsonify({
          '_id': str(ObjectId(user['_id'])),
          'name': user['name'],
          'description': user['description'],
          'url': user['url']
     })

@app.route('/tools/<id>', methods=['PUT'])
def edit_tool(id):
     db.tools.update_one({'_id': ObjectId(id)}, {'$set': {
          'name': request.json['name'],
          'description': request.json['description'],
          'url': request.json['url']
     }})

     return jsonify({'msg': 'Tool Updated'})

@app.route('/tools/<id>', methods=['DELETE'])
def delete_tool(id):
     db.tools.delete_one({'_id': ObjectId(id)})
     return jsonify({'msg': 'Tool Deleted'})




if __name__ == '__main__':
    app.run(debug=False)