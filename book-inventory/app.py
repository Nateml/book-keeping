from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/remove/<string:isbn>/<int:quantity>')
def remove_book(isbn, quantity):
    return jsonify({
        'message': f'removed {quantity} copies of book with isbn {isbn} from the system'
        }), 200

@app.route('/add/<string:isbn>/<int:quantity>')
def add_book(isbn, quantity):
    return jsonify({
        'message': f'added {quantity} copies of book with isbn {isbn} to the system'
        }), 200

@app.route('/set/<string:isbn>/<int:quantity>')
def set_quantity(isbn, quantity):
    return jsonify({
        'message': f'set quantity of book with isbn {isbn} to {quantity}'
        })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
