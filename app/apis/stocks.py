from flask_restplus import Namespace, Resource, fields, reqparse

from app import db
from app.models.stock import StockModel

api = Namespace('stocks', description='Stock related operations')

stock = api.model('Stock', {
    'store_id': fields.Integer(required=True, description='Store identifier'),
    'product_id': fields.Integer(required=True, description='Product identifier'),
    'quantity': fields.Integer(required=True, description='Stock quantity in store of a certain product'),
    # 'product': fields.Nested(product, required=False, description='Product object'),
})

parser = reqparse.RequestParser()
parser.add_argument('store_id', type=int, help='The store id')
parser.add_argument('product_id', type=int, help='The product id')


@api.route('/')
@api.response(404, 'Stock not found')
class StockList(Resource):

    @api.doc('list_stocks')
    @api.marshal_list_with(stock)
    @api.doc(parser=parser)
    def get(self):
        """List stocks given nothing or store_id and/or product_id"""
        args = parser.parse_args()
        store_id = args['store_id']
        product_id = args['product_id']

        if store_id is None and product_id is None:
            # find all stocks
            return StockModel.find_all()
        elif store_id is not None and product_id is None:
            # find stocks of certain store
            return StockModel.find_by_store(store_id)
        elif product_id is not None and store_id is None:
            # find stocks of certain product
            return StockModel.find_by_product(product_id)
        else:
            # find a certain stock of one product in one store
            _stock = StockModel.find_by_store_and_product(
                store_id=store_id,
                product_id=product_id
            )
            if _stock is not None:
                # stock found
                return [_stock]
            else:
                # stock not found
                api.abort(404)

    @api.doc('create_stock')
    @api.expect(stock, validate=True)
    @api.marshal_with(stock)
    def post(self):
        """Create new stock"""
        stock_found = StockModel.find_by_store_and_product(
            store_id=api.payload['store_id'],
            product_id=api.payload['product_id'],
        )
        if stock_found is None:
            new_stock = StockModel(
                store_id=api.payload['store_id'],
                product_id=api.payload['product_id'],
                quantity=api.payload['quantity']
            )
            db.session.add(new_stock)
            db.session.commit()
            return new_stock, 201
        api.abort(409)

    @api.doc('update_stock')
    @api.expect(stock, validate=True)
    @api.marshal_with(stock)
    def put(self):
        """Updates one stock of one product in a store"""
        # find stock
        stock_found = StockModel.find_by_store_and_product(
            store_id=api.payload['store_id'],
            product_id=api.payload['product_id'],
        )
        if stock_found is not None:
            # update stock quantity
            stock_found.quantity = api.payload['quantity']
            db.session.merge(stock_found)
            db.session.commit()
            return stock_found, 200
        api.abort(404)

    @api.doc('delete_stock')
    @api.doc(parser=parser)
    def delete(self):
        """Delete a stock"""
        args = parser.parse_args()
        store_id = args['store_id']
        product_id = args['product_id']

        if store_id is not None and product_id is not None:
            # find stock
            stock_found = StockModel.find_by_store_and_product(
                store_id=store_id,
                product_id=product_id,
            )
            if stock_found is not None:
                # delete stock
                db.session.delete(stock_found)
                db.session.commit()
                return '', 204
        api.abort(404)
