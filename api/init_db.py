import sqlite3
import json

# ...
DATABASE = "../data/app.db"

conn = sqlite3.connect(DATABASE)
with open('schema.sql') as f:
    conn.executescript(f.read())
conn.commit()
cur = conn.cursor()

# ...
with open("books.json", encoding='utf-8-sig') as json_file:
    data = json.loads(json_file.read())
    for item in data:
        conn.execute("INSERT INTO books (title, author, published) VALUES (?, ?, ?)", (item["title"], item["author"], item["published"]))
        conn.commit()

# ...
with open("users.json", encoding='utf-8-sig') as json_file:
    data = json.loads(json_file.read())
    for item in data:
        conn.execute("INSERT INTO users (username, password, firstname, lastname, email, city) VALUES (?, ?, ?, ?, ?, ?)", (item["username"], '123456', item["firstname"], item["lastname"], item["email"], item["city"]))
        conn.commit()
# ...
with open("crypto.json", encoding='utf-8-sig') as json_file:
    data = json.loads(json_file.read())
    for item in data:
        conn.execute("INSERT INTO crypto (name, ticker, price) VALUES (?, ?, ?)", (item["name"], item["ticker"], item["price"]))
        conn.commit()
        
# ...
with open("stocks.json", encoding='utf-8-sig') as json_file:
    data = json.loads(json_file.read())
    for item in data:
        conn.execute("INSERT INTO stocks (ticker, name, marketcap, price) VALUES (?, ?, ?, ?)", (item["ticker"], item["name"], item["marketcap"], item["price"]))
        conn.commit()

conn.close()
