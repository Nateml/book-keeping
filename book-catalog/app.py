from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

books = {}

@app.route('/book/', methods=['POST'])
def add_book():
    """ 
    Adds a new book to the system. 
    The post request should contain information about the book (isbn, title, author, date published). 
    Should we set the quantity of the book here or should we let the user make a seperate request to the book
        inventory microservice to set the quantity?
    """

    if not request.is_json:
        return jsonify({
            'message': 'Content type of request must be set to application/json'
            })

    data = request.json
    book = {
            data.get('isbn') :
                {
                    'isbn' : data.get('isbn'),
                    'title' : data.get('title'),
                    'author' : data.get('author'), 
                    'date_published' : data.get('date_published')
                }
           }

    books[isbn] = book[data.get('isbn')];

    return jsonify({
        'message' : 'Succesfully added book',
        'book' : book
        }), 200

@app.route('/book/<string:isbn>', methods=['GET', 'DELETE'])
def book(isbn):
    """ 
    Either returns the information of the book with the given isbn (in case of a GET request),
        or deletes the book from the system (in case of a DELETE request).
    """
    if request.method == 'GET':
        try:
            return jsonify(books[isbn]),200
        except:
            return jsonify({
                    'message': 'Invalid request'
                }),400
    elif request.method == 'DELETE':
        try:
            return jsonify({
                    'message' : f'Succesfully deleted book with isbn: {isbn}',
                    'book' : books.pop(isbn)
                    }), 200
        except:
            return jsonify({
                    'message' : 'Invalid request'
                    }),400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)


