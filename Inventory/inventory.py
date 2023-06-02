from flask import Flask
from flask import jsonify
from json import load, dump
import os

app = Flask(__name__)

MOCK_DATA_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\data.json"

def overwrite_json_file(json_data, out_file):
    with open(out_file, "w") as f:
        dump(json_data, f, indent=4)

@app.route('/inventory/quantity/<string:isbn>')
def get_quantity(isbn):
    """
    Returns the quantity of a book with the given isbn.
    """
    # input validation
    if not isinstance(isbn, str):
        return jsonify({
            'message': 'Invalid request'
        }),400

    books = load(open(MOCK_DATA_PATH))

    if not isbn in books['inventory']:
        return jsonify({
            'message': f'Book with isbn: {isbn}, does not exist'
        }),400

    try:
        return jsonify({
            'isbn' : isbn,
            'quantity' : books["inventory"][isbn]
        }),200 # simple enough
    except Exception as e:
        print(e)
        return jsonify({
                'message' : 'Invalid request'
                }),400

@app.route('/inventory/remove/<string:isbn>/<int:quantity>')
def remove_book(isbn, quantity):
    """
    Removes x copies of a book from the inventory.
    """
    # input validation
    if not isinstance(isbn, str) or not isinstance(quantity, int):
        return jsonify({
            'message': 'Invalid request'
        }),400

    books = load(open(MOCK_DATA_PATH))

    if not isbn in books['inventory']:
        return jsonify({
            'message': f'Book with isbn: {isbn}, does not exist'
        }),400

    try:
        if isbn in books["inventory"] and books["inventory"][isbn] >= quantity: # check if book actually exists in the inventory, and that there are enough copies of the book to remove
            books["inventory"][isbn] -= quantity
        else:
            raise Exception

        overwrite_json_file(books, MOCK_DATA_PATH)

        return jsonify({
            'message': f'removed {quantity} copies of book with isbn {isbn} from the system'
            }), 200
    except Exception as e:
        print(e)
        return jsonify({
                'message' : 'Invalid request'
                }),400

@app.route('/inventory/add/<string:isbn>/<int:quantity>')
def add_book(isbn, quantity):
    """
    Adds x copies of a book to the inventory.
    """
    # input validation
    if not isinstance(isbn, str) or not isinstance(quantity, int):
        return jsonify({
            'message': 'Invalid request'
        }),400

    books = load(open(MOCK_DATA_PATH))

    if not isbn in books['inventory']:
        return jsonify({
            'message': f'Book with isbn: {isbn}, does not exist'
        }),400

    try:
        if not isbn in books["inventory"]: # if the book does not exist in the inventory, add it
            books["inventory"][isbn] = 0
        books["inventory"][isbn] += quantity

        overwrite_json_file(books, MOCK_DATA_PATH)

        return jsonify({
            'message': f'added {quantity} copies of book with isbn {isbn} to the system'
            }), 200
    except Exception as e:
        print(e)
        return jsonify({
                'message' : 'Invalid request'
                }),400

@app.route('/inventory/set/<string:isbn>/<int:quantity>')
def set_quantity(isbn, quantity):
    # input validation
    if not isinstance(isbn, str) or not isinstance(quantity, int):
        return jsonify({
            'message': 'Invalid request'
        }),400

    books = load(open(MOCK_DATA_PATH))

    if not isbn in books['inventory']:
        return jsonify({
            'message': f'Book with isbn: {isbn}, does not exist'
        }),400

    try:
        books["inventory"][isbn] = quantity
        overwrite_json_file(books, MOCK_DATA_PATH)
        return jsonify({
            'message': f'set quantity of book with isbn {isbn} to {quantity}'
            })
    except Exception as e:
        print(e)
        return jsonify({
                'message' : 'Invalid request'
                }),400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3002)
