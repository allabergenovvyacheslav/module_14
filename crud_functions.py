# Создайте файл crud_functions.py и напишите там следующие функции:
# initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса.
# Эта таблица должна содержать следующие поля:

# id - целое число, первичный ключ
# title(название продукта) - текст (не пустой)
# description(описание) - тест
# price(цена) - целое число (не пустой)

# get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.

import sqlite3

con = sqlite3.connect('Products.db')
cur = con.cursor()


def initiate_db():

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    descriptions TEXT,
    price INT NOT NULL
    );
    ''')


def get_all_products(title, descriptions, price):

    all_product = 'SELECT * FROM Products'
    if all_product is None:
        for x in range(1, 5):
            cur.execute(f'''
            INSERT INTO VALUES ('{title[x]}', '{descriptions[x]}', '{price[x*100]}')
            ''')
            con.commit()
    return all_product


con.commit()
con.close()