from flask_restplus import Api

from .products import api as product_api
from .stocks import api as stock_api
from .stores import api as store_api

api = Api(
    title='Flask Store REST API',
    version='1.0',
    description='This is an example of REST API with Flask-RESTPlus',
)

api.add_namespace(product_api)
api.add_namespace(store_api)
api.add_namespace(stock_api)
