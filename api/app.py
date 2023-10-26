from flask import Flask, request, jsonify, render_template, url_for, flash, redirect, make_response
from flask_cors import CORS, cross_origin
import sqlite3
import sys
import os

# ...
DATABASE = '../data/app.db'

# ...
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# 
# utilities
#
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# ...
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = make_dicts
    return conn

# ...
def not_found():
    return make_response(jsonify([]), 200)

# ...
@app.errorhandler(404)
def page_not_found(e):
    return not_found()

def fetch_all(table):
    conn = get_db_connection()
    result = conn.execute(f'SELECT * FROM {table}').fetchall()
    conn.close()
    if result is None:
        return not_found()
    return jsonify(result)

# 
# books
#
@app.route('/api/v1/books', methods=['GET'])
def all_books():
    return fetch_all('books')

# ...
@app.route("/api/v1/books", methods=['POST'])
def create_book():
    book = request.get_json()
    print(book)
    if not book['title']:
        flash('Title is required!')
    elif not book['author']:
        flash('Author is required!')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, published) VALUES (?, ?, ?)', (book['title'], book['author'], book['published']))
        conn.commit()
        conn.close()
        return all_books()

# ...
@app.route('/api/v1/books/<int:id>', methods=['GET'])
def one_book():
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()
    conn.close()
    if result is None:
        return not_found()
    return jsonify(result)

# 
# users
#
@app.route('/api/v1/users', methods=['GET'])
def all_users():
    return fetch_all('users')
    
# 
# crypto
#
@app.route('/api/v1/crypto', methods=['GET'])
def all_crypto():
    return fetch_all('crypto')
    
# 
# stocks
#
@app.route('/api/v1/stocks', methods=['GET'])
def all_stocks():
    return fetch_all('stocks')
        
# 
# main
#
if __name__ == '__main__':
    if os.environ.get('PORT') is not None:
        app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
    else:
        app.run(debug=True, host='0.0.0.0')
