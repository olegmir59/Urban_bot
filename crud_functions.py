"""
#           Для автономной работы с базой в crud_functions.py
import sqlite3

connection = sqlite3.connect("bot_database.db")
cursor = connection.cursor()
"""




def initiate_db(connection, cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age  TEXT NOT NULL,
    balance TEXT NOT NULL
    )
    ''')
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")

    connection.commit()


def get_all_products(cursor):
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    return products


def add_user(connection, cursor, username, email, age):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (username, email, age, 1000))
    connection.commit()


def is_included(cursor, username):
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchall()
    if user:
        return True
    else:
        return False


"""
#           Для автономной работы с базой в crud_functions.py

products_list = get_all_products(cursor)

for product in products_list:
    print(f"title: {product[1]} | description: {product[2]} |  price: {product[3]}")


for i in range(1, 5):
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   (f"Продукт {i}", f"Витамин  номер {i}", i*200))
                   

for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)", (f"User{i}", f"example{i}@gmail.com", i*10, 1000))

                   

initiate_db(connection, cursor)

#add_user(connection, cursor, "username", "email", 35)
connection.commit()
connection.close()
"""

