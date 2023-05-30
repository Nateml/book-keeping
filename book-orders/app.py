from flask import Flask
from flask import jsonify
import requests

app = Flask(__name__)

orders = {}
identifer = 1

@app.route('/orders/<string:isbn>/<int:quantity>/<string:date>')
def order(isbn, quantity, date):
    """ 
    This method should place an order for x copies of a book with the given isbn (if it exists). 
    This means the book inventory should reflect that there are x less copies of the book available after the order.
    """
    try:
        # adjust inventory:
        r = requests.get(url=f'http://localhost:3000/inventory/remove/{isbn}/{quantity}')
        if r.status_code != 200:
            raise Exception # do not place order if there was an error updating inventory

        orders[identifer] = {
            'isbn' : isbn,
            'quantity' : quantity,
            'date' : date
        }
        identifer += 1 # increase identifier so that the next order has a unique ID

        return jsonify({
            'message': f'placed order for {quantity} copies of {isbn} on {date}'
            }), 200

    except Exception as e:
        print(e)
        return jsonify({
                'message' : 'Invalid request'
                }),400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3003)
