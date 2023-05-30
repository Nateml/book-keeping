from flask import Flask
from flask import request
from flask import jsonify
import requests

app = Flask(__name__)

books = {}

@app.route('/catalog/book/', methods=['POST'])
def add_book():
    """ 
    Adds a new book to the system. 
    The post request should contain information about the book (isbn, title, author, date published). 
    Should we set the quantity of the book here or should we let the user make a seperate request to the book
        inventory microservice to set the quantity?
    """
    try:
        if not request.is_json: # check if the post request body is in json format
            return jsonify({
                'message': 'Content type of request must be set to application/json'
                })
        

        # add book:
        data = request.json
        book = {
                data.get('isbn') :
                    {
                        'isbn' : data.get('isbn'),
                        'title' : data.get('title'),
                        'author' : data.get('author'), 
                        'date_published' : data.get('date_published'),
                    }
            }

        books[data.get('isbn')] = book[data.get('isbn')]

        # set quantity
        r = requests.get(url=f'http://localhost:3000/inventory/add/{data.get("isbn")}/{data.get("quantity")}')
        if r.status_code != 200:
            raise Exception

        return jsonify({
            'message' : 'Succesfully added book',
            'book' : book
            }), 200

    except Exception as e:
        print(e)
        return jsonify({
                'message' : 'Invalid request'
                }),400

@app.route('/catalog/book/<string:isbn>', methods=['GET', 'DELETE', 'PUT'])
def book(isbn):
    """ 
    Either returns the information of the book with the given isbn (in case of a GET request),
        or deletes the book from the system (in case of a DELETE request).
    """
    if request.method == 'GET':
        try:
            return jsonify(books[isbn]),200
        except Exception as e:
            print(e)
            return jsonify({
                    'message': 'Invalid request'
                }),400
    elif request.method == 'DELETE':
        try:
            r = requests.get(url=f'http://localhost:3000/inventory/set/{data.get("isbn")}/0')
            if r.status_code != 200:
                raise Exception # do not continue if there was an error updating the inventory

            return jsonify({
                    'message' : f'Succesfully deleted book with isbn: {isbn}',
                    'book' : books.pop(isbn)
                    }), 200
        except Exception as e:
            print(e)
            return jsonify({
                    'message' : 'Invalid request'
                    }),400
    elif request.method == 'PUT':
        try:
            data = request.json
            book = {
                'isbn' : isbn,
                'title' : data.get('title'),
                'author' : data.get('author'),
                'date_published' : data.get('date_published')
            }
            books[isbn] = book
            return jsonify({
                    'message' : f'Succesfully updated book with isbn: {isbn}',
                    'book' : books[isbn]
                    }), 200
        except Exception as e:
            print(e)
            return jsonify({
                    'message' : 'Invalid request'
                    }),400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)


