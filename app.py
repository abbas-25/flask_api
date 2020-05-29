from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'abbas'
api = Api(app)


# create table and add all the tables needed in it
@app.before_first_request
def create_tables():
    db.create_all()


# creates a endpoint /auth that runs authenticate method
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")

api.add_resource(ItemList, "/items")

api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

db.init_app(app)
if __name__ == '__main__':
    app.run(port=5000, debug=True)
