from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/order/<string:isbn>/<int:quantity>')
def order(isbn, quantity):
    """ 
    This method should place an order for x copies of a book with the given isbn (if it exists). 
    This means the book inventory should reflect that there are x less copies of the book available after the order.
    """
    return jsonify({
        'message': f'placed order for {quantity} copies of {isbn}'
        }), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
