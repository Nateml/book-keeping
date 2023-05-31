from flask import Flask
from flask import request
from flask import jsonify
from json import load, dump

app = Flask(__name__)

MOCK_DATA_PATH = "../data.json"

def overwrite_json_file(json_data, out_file):
    with open(out_file, "w") as f:
        dump(json_data, f, indent=4)

@app.route('/catalog/book/', methods=['POST'])
def add_book():
    """ 
    Adds a new book to the system. 
    The post request should contain information about the book (isbn, title, author, date published, quantity). 
    Should we set the quantity of the book here or should we let the user make a seperate request to the book
        inventory microservice to set the quantity?
    """

    books = load(open(MOCK_DATA_PATH))

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

        books["catalog"][data.get('isbn')] = book[data.get('isbn')]

        # set quantity
        books["inventory"][data.get('isbn')] = data.get('quantity')

        overwrite_json_file(books, MOCK_DATA_PATH)

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

    books = load(open(MOCK_DATA_PATH))

    if request.method == 'GET':
        try:
            return jsonify(books["catalog"][isbn]),200
        except Exception as e:
            print(e)
            return jsonify({
                    'message': 'Invalid request'
                }),400

    elif request.method == 'DELETE':
        try:
            quantity = books["inventory"].pop(isbn)
            book = books["catalog"].pop(isbn)

            overwrite_json_file(books, MOCK_DATA_PATH)

            return jsonify({
                    'message' : f'Succesfully deleted book with isbn: {isbn}',
                    'book' : book
                    }), 200

        except Exception as e:
            # revert any changes to book data:
            books["inventory"][isbn] = quantity
            books["catalog"][isbn] = book
            
            overwrite_json_file(books, MOCK_DATA_PATH)

            print(e)
            return jsonify({
                    'message' : 'Invalid request'
                    }),400

    elif request.method == 'PUT':
        try:
            old_book = books["catalog"][isbn]

            data = request.json

            book = {
                'isbn' : isbn,
                'title' : data.get('title'),
                'author' : data.get('author'),
                'date_published' : data.get('date_published')
            }

            books["catalog"][isbn] = book

            overwrite_json_file(books, MOCK_DATA_PATH)

            return jsonify({
                    'message' : f'Succesfully updated book with isbn: {isbn}',
                    'book' : books["catalog"][isbn]
                    }), 200

        except Exception as e:
            # revert any changes to books data:
            books["catalog"][isbn] = old_book
            overwrite_json_file(books, MOCK_DATA_PATH)
            print(e)
            return jsonify({
                    'message' : 'Invalid request'
                    }),400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)


