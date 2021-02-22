from flask_restplus import Namespace, Resource, fields

from app import db
from app.models.store import StoreModel, StoreSchema
from .stocks import stock

api = Namespace('stores', description='Store related operations')

store = api.model('Store', {
    'id': fields.String(required=False, description='Store identifier'),
    'name': fields.String(required=True, description='Store name'),
    'phone': fields.String(required=True, description='Store phone number'),
    'email': fields.String(required=True, description='Store email contact'),
    'address': fields.String(required=True, description='Store address'),
    'city': fields.String(required=True, description='Store city'),
    'state': fields.String(required=True, description='Store state'),
    'zip_code': fields.String(required=True, description='Store zip code'),
    'stocks': fields.List(fields.Nested(stock)),
})

schema = StoreSchema()


@api.route('/')
class StoreList(Resource):
    @api.doc('list_stores')
    @api.marshal_list_with(store)
    def get(self):
        """List all stores"""
        return StoreModel.find_all()

    @api.doc('create_store')
    @api.expect(store, validate=True)
    @api.marshal_with(store)
    def post(self):
        """Create new store"""
        new_store = schema.load(api.payload)
        db.session.add(new_store)
        db.session.commit()
        return new_store, 201


@api.route('/<id>')
@api.param('id', 'The store identifier')
@api.response(404, 'Store not found')
class Store(Resource):
    @api.doc('get_store')
    @api.marshal_with(store)
    def get(self, id):
        """Fetch a store given its id"""
        store_found = StoreModel.find_by_id(id)
        if store_found is not None:
            return store_found
        api.abort(404)

    @api.doc('update_store')
    @api.expect(store, validate=False)
    @api.marshal_with(store)
    def put(self, id):
        """Updates a store"""
        store_found = StoreModel.find_by_id(id)
        if store_found is not None:
            updated_store = schema.load(api.payload)
            updated_store.id = store_found.id
            db.session.merge(updated_store)
            db.session.commit()
            return StoreModel.find_by_id(id), 200
        api.abort(404)

    @api.doc('delete_store')
    def delete(self, id):
        """Delete a store"""
        store_found = StoreModel.find_by_id(id)
        if store_found is not None:
            db.session.delete(store_found)
            db.session.commit()
            return '', 204
        api.abort(404)
