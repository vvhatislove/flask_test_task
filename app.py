import os

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import dotenv

dotenv.load_dotenv('.env')

DB_HOST = os.getenv('DB_HOST', default='localhost')
app = Flask(__name__)
app.config['DEBUG'] = True
# if you are running via docker DB_HOST should be "mongo"
app.config["MONGO_URI"] = f"mongodb://{DB_HOST}:27017/data_db"
mongo = PyMongo(app)


@app.route("/key", methods=["GET", "POST", "PUT"])
def handle_key():
    if request.method == "POST":
        key = request.form.get("key")
        value = request.form.get("value")
        mongo.db.data.insert_one({"key": key, "value": value})
        return "Key-value pair created.", 201
    elif request.method == "PUT":
        key = request.form.get("key")
        value = request.form.get("value")
        mongo.db.data.update_one({"key": key}, {"$set": {"value": value}})
        return "Key-value pair updated.", 200
    else:
        key = request.args.get("key")
        result = mongo.db.data.find_one({"key": key})
        if result:
            result.pop('_id')
            return jsonify(result), 200
        else:
            return "Key not found.", 404


if __name__ == "__main__":
    app.run(debug=True, port=8080)
