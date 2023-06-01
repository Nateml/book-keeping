import pytest
import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Catalog.catalog import app
import os
from json import load
from flask.testing import FlaskClient

data_file_path = os.getcwd() + "\\data.json"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get(client : FlaskClient):
    data = load(open(data_file_path))
    book = data["catalog"]["123"]
    rv = client.get('/catalog/book/123')
    assert bytes(book["title"], 'UTF-8') in rv.data and bytes(book["author"], 'UTF-8') in rv.data and bytes(book["date_published"], 'UTF-8') in rv.data

def test_add(client : FlaskClient):
    book = {
        'isbn' : '1',
        'title' : 'Test Book',
        'author' : 'Test Author',
        'date_published' : '01012001',
        'quantity' : 10
    }
    rv = client.post('/catalog/book/', json=book)
    data = load(open(data_file_path))
    assert rv.status_code == 200 and bytes(book['isbn'], 'UTF-8') in rv.data and bytes(book['title'], 'UTF-8') in rv.data and data['inventory'][book['isbn']] == book['quantity']

def test_put(client : FlaskClient):
    book = {
        'isbn' : '1',
        'title' : 'Test Book',
        'author' : 'Test Author 2',
        'date_published' : '01012001',
    }
    rv = client.put('/catalog/book/1', json=book)
    data = load(open(data_file_path))
    assert rv.status_code == 200 and data['catalog']['1']['author'] == 'Test Author 2'

def test_delete(client : FlaskClient):
    rv = client.delete('/catalog/book/1')
    data = load(open(data_file_path))
    assert rv.status_code == 200 and '1' not in dict(data['catalog']).keys() and '1' not in dict(data['inventory']).keys()

