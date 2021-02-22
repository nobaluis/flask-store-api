import pytest

from app import create_app, db
from app.models.product import ProductModel
from app.models.stock import StockModel
from app.models.store import StoreModel


@pytest.fixture(scope="module")
def test_app():
    app = create_app('test')
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_db():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="function")
def add_product():
    def _add_product(sku, name, brand, model, price):
        product = ProductModel(sku=sku, name=name, brand=brand, model=model, price=price)
        db.session.add(product)
        db.session.commit()
        return product

    return _add_product


@pytest.fixture(scope="function")
def add_store():
    def _add_store(name, phone, email, address, city, state, zip_code):
        store = StoreModel(name=name, phone=phone, email=email, address=address, city=city, state=state,
                           zip_code=zip_code)
        db.session.add(store)
        db.session.commit()
        return store

    return _add_store


@pytest.fixture(scope="function")
def add_stock():
    def _add_stock(store_id, product_id, quantity):
        stock = StockModel(store_id=store_id, product_id=product_id, quantity=quantity)
        db.session.add(stock)
        db.session.commit()
        return stock

    return _add_stock
