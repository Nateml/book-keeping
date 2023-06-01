import pytest
import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Orders.orders import app
import os
from json import load
from flask.testing import FlaskClient

data_file_path = os.getcwd() + "\\data.json"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_order(client : FlaskClient):
    initial_data = load(open(data_file_path))
    rv = client.get('/orders/123/1/01012023')
    data = load(open(data_file_path))
    assert rv.status_code == 200 and b'placed order for 1 copies of 123 on 01012023' in rv.data and data['inventory']['123'] + 1 == initial_data['inventory']['123']

def test_bad_order(client : FlaskClient):
    initial_data = load(open(data_file_path))
    rv = client.get(f'/orders/123/{initial_data["inventory"]["123"]+1}/01012023')
    assert rv.status_code == 400 and b'Invalid request' in rv.data
