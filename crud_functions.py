import sqlite3

def initiate_db():
    connection = sqlite3.connect("bot_database.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL
    );
    ''')
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect("bot_database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products


"""
connection = sqlite3.connect("bot_database.db")
cursor = connection.cursor()
for i in range(1, 5):
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   (f"Продукт {i}", f"Витамин  номер {i}", i*200))

connection.commit()
connection.close()
"""

