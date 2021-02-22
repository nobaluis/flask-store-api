import json

from app.models.product import ProductModel
from app.models.stock import StockModel
from app.models.store import StoreModel


def clean_tables(_db):
    _db.session.query(StockModel).delete()
    _db.session.query(StoreModel).delete()
    _db.session.query(ProductModel).delete()


def test_create_stock(test_app, test_db, add_store, add_product):
    clean_tables(test_db)
    store = add_store('foo store', '123456789', 'foo@email.com', 'foo street', 'foo city', 'foo state', '12345')
    product = add_product('DEF456', 'boo', 'boo co', 'boo model', 11.0)
    client = test_app.test_client()
    payload = {
        'store_id': store.id,
        'product_id': product.id,
        'quantity': 10
    }
    resp = client.post(
        '/stocks/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    for key in payload:
        assert payload[key] == data[key]


def test_get_stock(test_app, test_db, add_store, add_product, add_stock):
    clean_tables(test_db)
    store = add_store('foo store', '123456789', 'foo@email.com', 'foo street', 'foo city', 'foo state', '12345')
    product = add_product('DEF456', 'boo', 'boo co', 'boo model', 11.0)
    add_stock(store.id, product.id, 20)
    client = test_app.test_client()
    resp = client.get(f'/stocks/?store_id={store.id}&product_id={product.id}')
    data = json.loads(resp.data.decode())[0]
    assert resp.status_code == 200
    assert store.id == data['store_id']
    assert product.id == data['product_id']
    assert 20 == data['quantity']


def test_get_stocks(test_app, test_db, add_store, add_product, add_stock):
    clean_tables(test_db)
    store = add_store('foo store', '123456789', 'foo@email.com', 'foo street', 'foo city', 'foo state', '12345')
    product_a = add_product('ABC123', 'foo', 'foo co', 'foo model', 10.0)
    product_b = add_product('DEF456', 'boo', 'boo co', 'boo model', 11.0)
    add_stock(store.id, product_a.id, 10)
    add_stock(store.id, product_b.id, 20)
    client = test_app.test_client()
    resp = client.get('/stocks/')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2


def test_update_stock(test_app, test_db, add_store, add_product, add_stock):
    clean_tables(test_db)
    store = add_store('foo store', '123456789', 'foo@email.com', 'foo street', 'foo city', 'foo state', '12345')
    product = add_product('DEF456', 'boo', 'boo co', 'boo model', 11.0)
    add_stock(store.id, product.id, 20)
    client = test_app.test_client()
    payload = {
        'store_id': store.id,
        'product_id': product.id,
        'quantity': 10
    }
    resp = client.put(
        f'/stocks/',
        data=json.dumps(payload),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    for key in payload:
        assert payload[key] == data[key]


def test_delete_stock(test_app, test_db, add_store, add_product, add_stock):
    clean_tables(test_db)
    store = add_store('foo store', '123456789', 'foo@email.com', 'foo street', 'foo city', 'foo state', '12345')
    product = add_product('DEF456', 'boo', 'boo co', 'boo model', 11.0)
    add_stock(store.id, product.id, 20)

    client = test_app.test_client()
    resp_one = client.get(f'/stocks/?store_id={store.id}&product_id={product.id}')
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f'/stocks/?store_id={store.id}&product_id={product.id}')
    assert resp_two.status_code == 204

    resp_three = client.get('/stocks/')
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0
