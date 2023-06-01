import pytest
import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Inventory.inventory import app
import os
from json import load
from flask.testing import FlaskClient

data_file_path = os.getcwd() + "\\data.json"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_set(client : FlaskClient):
    rv = client.get('/inventory/set/123/10')
    data = load(open(data_file_path))
    assert rv.status_code == 200 and data['inventory']['123'] == 10

def test_get(client : FlaskClient):
    rv = client.get('/inventory/quantity/123')
    assert b'10' in rv.data

def test_add(client : FlaskClient):
    rv = client.get('/inventory/add/123/1')
    data = load(open(data_file_path))
    assert rv.status_code == 200 and b'added 1 copies of book with isbn 123 to the system' in rv.data and data['inventory']['123'] == 11

def test_remove(client : FlaskClient):
    rv = client.get('/inventory/remove/123/1')
    data = load(open(data_file_path))
    assert rv.status_code == 200 and b'removed 1 copies of book with isbn 123 from the system' in rv.data and data['inventory']['123'] == 10
