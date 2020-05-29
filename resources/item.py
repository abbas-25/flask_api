from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="This field can not be blank!")
    parser.add_argument('store_id', type=float, required=True,
                        help="This field can not be blank!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.findByName(name)

        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.findByName(name):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item!'}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.findByName(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.findByName(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
