import json

from app.models.store import StoreModel


def test_create_store(test_app, test_db):
    client = test_app.test_client()
    payload = {
        'name': 'foo store',
        'phone': '123456789',
        'email': 'foo@email.com',
        'address': 'foo street',
        'city': 'foo city',
        'state': 'foo state',
        'zip_code': '12345'
    }
    resp = client.post(
        '/stores/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    for key in payload:
        assert payload[key] == data[key]


def test_get_store(test_app, test_db, add_store):
    store = add_store('boo store', '987456321', 'boo@email.com', 'boo street', 'boo city', 'boo state', '54321')
    client = test_app.test_client()
    resp = client.get(f'/stores/{store.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'boo store' in data['name']
    assert '987456321' in data['phone']
    assert 'boo@email.com' in data['email']
    assert 'boo street' in data['address']
    assert 'boo city' in data['city']
    assert 'boo state' in data['state']
    assert '54321' in data['zip_code']


def test_get_stores(test_app, test_db, add_store):
    test_db.session.query(StoreModel).delete()
    add_store('foo store', '123456789', 'foo@email.com', 'foo street', 'foo city', 'foo state', '12345')
    add_store('boo store', '987456321', 'boo@email.com', 'boo street', 'boo city', 'boo state', '54321')
    client = test_app.test_client()
    resp = client.get('/stores/')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2


def test_update_store(test_app, test_db, add_store):
    store = add_store('cool store', '123456788', 'cool@email.com', 'cool street', 'cool city', 'cool state', '12346')
    client = test_app.test_client()
    payload = {
        'name': 'uncool store',
        'phone': '123456789',
        'email': 'uncool@email.com',
        'address': 'uncool street',
        'city': 'uncool city',
        'state': 'uncool state',
        'zip_code': '11111'
    }
    resp_one = client.put(
        f'/stores/{store.id}',
        data=json.dumps(payload),
        content_type='application/json',
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    for key in payload:
        assert payload[key] == data[key]


def test_delete_store(test_app, test_db, add_store):
    test_db.session.query(StoreModel).delete()
    store = add_store('foo store', '123456789', 'foo@email.com', 'foo street', 'foo city', 'foo state', '12345')
    client = test_app.test_client()
    resp_one = client.get('/stores/')
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f'/stores/{store.id}')
    assert resp_two.status_code == 204

    resp_three = client.get('/stores/')
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0
