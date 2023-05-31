from flask import Flask
from flask import jsonify
import requests
from json import load, dump

app = Flask(__name__)

MOCK_DATA_PATH = "../data.json"

def overwrite_json_file(json_data, out_file):
    with open(out_file, "w") as f:
        dump(json_data, f, indent=4)

def remove_copies(isbn:str, quantity:int, books:dict):
    if books["inventory"][isbn] < quantity:
        raise Exception
    books["inventory"][isbn] -= quantity

@app.route('/orders/<string:isbn>/<int:quantity>/<string:date>')
def order(isbn, quantity, date):
    """ 
    This method should place an order for x copies of a book with the given isbn (if it exists). 
    This means the book inventory should reflect that there are x less copies of the book available after the order.
    """
    try:
        books = load(open(MOCK_DATA_PATH))

        # adjust inventory:
        remove_copies(isbn, quantity, books)

        overwrite_json_file(books, MOCK_DATA_PATH)

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
