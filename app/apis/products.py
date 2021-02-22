from flask_restplus import Namespace, Resource, fields

from app import db
from app.models.product import ProductModel, ProductSchema

api = Namespace('products', description='Products related operations')

product = api.model('Product', {
    'id': fields.String(required=False, description='Product db identifier'),
    'sku': fields.String(required=True, description='Product warehouse ref'),
    'name': fields.String(required=True, description='Product name'),
    'brand': fields.String(required=True, description='Product manufacturer'),
    'model': fields.String(required=True, description='Product model/year/serial no.'),
    'price': fields.Float(required=True, description='Product list price')
})

schema = ProductSchema()


@api.route('/')
class ProductList(Resource):
    @api.doc('list_products')
    @api.marshal_list_with(product)
    def get(self):
        """List all products"""
        return ProductModel.find_all()

    @api.doc('create_product')
    @api.expect(product, validate=True)
    @api.marshal_with(product)
    def post(self):
        """Create new product"""
        product_exist = ProductModel.find_by_sku(api.payload['sku'])
        if product_exist is None:
            new_product = schema.load(api.payload)
            db.session.add(new_product)
            db.session.commit()
            return new_product, 201
        api.abort(409)


@api.route('/<id>')
@api.param('id', 'The product identifier')
@api.response(404, 'Product not found')
class Product(Resource):
    @api.doc('get_product')
    @api.marshal_with(product)
    def get(self, id):
        """Fetch a product given its id"""
        product_found = ProductModel.find_by_id(id)
        if product_found is not None:
            return product_found
        api.abort(404)

    @api.doc('update_product')
    @api.expect(product, validate=False)
    @api.marshal_with(product)
    def put(self, id):
        """Updates a product"""
        product_found = ProductModel.find_by_id(id)
        if product_found is not None:
            updated_product = schema.load(api.payload)
            updated_product.id = product_found.id
            db.session.merge(updated_product)
            db.session.commit()
            return ProductModel.find_by_id(id), 200
        api.abort(404)

    @api.doc('delete_product')
    def delete(self, id):
        """Delete a product"""
        product_found = ProductModel.find_by_id(id)
        if product_found is not None:
            db.session.delete(product_found)
            db.session.commit()
            return '', 204
        api.abort(404)
