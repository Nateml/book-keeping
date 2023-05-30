from flask import Flask
from flask import jsonify

app = Flask(__name__)

books = {}

@app.route('/inventory/quantity/<string:isbn>')
def get_quantity(isbn):
    """
    Returns the quantity of a book with the given isbn.
    """
    try:
        return jsonify({
            'isbn' : isbn,
            'quantity' : books[isbn]
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
    try:
        if isbn in books and books[isbn] >= quantity: # check if book actually exists in the inventory, and that there are enough copies of the book to remove
            books[isbn] -= quantity
        else:
            raise Exception

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
    try:
        if not isbn in books: # if the book does not exist in the inventory, add it
            books[isbn] = 0
        books[isbn] += quantity

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
    try:
        books[isbn] = quantity
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
