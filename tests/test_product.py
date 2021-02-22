import json

from app.models.product import ProductModel


def test_create_product(test_app, test_db):
    client = test_app.test_client()
    payload = {
        'sku': 'ABC123',
        'name': 'foo product',
        'brand': 'foo co',
        'model': 'foo model',
        'price': 10.0
    }
    resp = client.post(
        '/products/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    for key in payload:
        assert payload[key] == data[key]


def test_get_product(test_app, test_db, add_product):
    product = add_product('DEF456', 'boo', 'boo co', 'boo model', 11.0)
    client = test_app.test_client()
    resp = client.get(f'/products/{product.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'DEF456' in data['sku']
    assert 'boo' in data['name']


def test_get_products(test_app, test_db, add_product):
    test_db.session.query(ProductModel).delete()
    add_product('ABC123', 'foo', 'foo co', 'foo model', 10.0)
    add_product('DEF456', 'boo', 'boo co', 'boo model', 11.0)
    client = test_app.test_client()
    resp = client.get('/products/')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2


def test_update_product(test_app, test_db, add_product):
    product = add_product('XYZ123', 'cool product', 'cool co', 'C001', 101.0)
    client = test_app.test_client()
    payload = {
        'name': 'uncool product',
        'brand': 'uncool co',
        'model': 'UC001',
        'price': 1.0
    }
    resp_one = client.put(
        f'/products/{product.id}',
        data=json.dumps(payload),
        content_type='application/json',
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    for key in payload:
        assert payload[key] == data[key]


def test_delete_product(test_app, test_db, add_product):
    test_db.session.query(ProductModel).delete()
    product = add_product('ABC123', 'foo', 'foo co', 'foo model', 10.0)
    client = test_app.test_client()
    resp_one = client.get('/products/')
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f'/products/{product.id}')
    assert resp_two.status_code == 204

    resp_three = client.get('/products/')
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0
