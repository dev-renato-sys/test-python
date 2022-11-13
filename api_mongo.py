from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
# from api_constants import mongodb_password
from datetime import date
from mongoengine import *
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
database_name = "YOUR_DATABASE_NAME_GOES_HERE"
mongodb_password = "YOUR_PASSWORD_GOES_HERE"
DB_URI = "mongodb+srv://erp-system:{}@cluster0.fiotm.mongodb.net/{}?retryWrites=true&w=majority".format(
    mongodb_password, database_name)
app.config["MONGODB_HOST"] = DB_URI


db = MongoEngine()
db.init_app(app)


class Product(db.Document):
    name = StringField(max_length=200, required=True)
    createdAt = DateField(required=True, default=date.today())

    def to_json(self, *args, **kwargs):
        return {
            # "id": self.id,
            "name": self.name,
            "createdAt": self.createdAt
        }


@app.route('/api/product', methods=['GET', 'POST'])
def api_product():
    if request.method == "GET":
        products = []
        for product in Product.objects:
            products.append(product)
        return make_response(jsonify(products), 200)
    elif request.method == "POST":
        content = request.json
        product = Product(name=content["name"])
        print(content, product)
        product.save()
        return make_response("success", 201)


@app.route('/api/product/<product_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_product(product_id):
    if request.method == "GET":
        product = Product.objects(id=product_id).first()
        if (product):
            return make_response(jsonify(product.to_json()), 200)
        else:
            return make_response("products not founded", 404)
    elif request.method == "PUT":
        content = request.json
        product = Product.objects(id=product_id).first()
        product.update(name=content["name"])
        return make_response("sucess", 200)
    elif request.method == "DELETE":
        product = Product.objects(id=product_id).first()
        product.delete()
        return make_response("sucess", 204)


if __name__ == '__main__':
    app.run()
