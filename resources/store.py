from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.findByName(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        store = StoreModel.findByName(name)
        if store:
            return {'message': 'Store already exists'}
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'an error occured while adding new store'}, 500
        
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.findByName(name)
        if store:
            store.delete_from_db()
            
        return {'message': 'store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
