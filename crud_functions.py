# -*- coding: utf-8 -*-

# Создайте файл crud_functions.py и напишите там следующие функции:
# initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса.
# Эта таблица должна содержать следующие поля:

# id - целое число, первичный ключ
# title(название продукта) - текст (не пустой)
# description(описание) - тест
# price(цена) - целое число (не пустой)

# get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи
# SQL запроса.

import sqlite3

connection = sqlite3.connect('database_14.db')
cursor = connection.cursor()

cursor.executescript('''
CREATE TABLE IF NOT EXISTS Products(
id INT PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INT NOT NUll
);
CREATE TABLE IF NOT EXISTS Users(
id INT PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INT NOT NUll,
balance INT NOT NUll
);
''')


def get_all_products():
    all_products = cursor.execute('SELECT * FROM Products;').fetchall()
    connection.commit()
    return all_products


def add_products():
    for prod in range(1, 5):
        cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                       (f'Product{prod}',
                        f'Description{prod}',
                        f'Price{prod * 100}'))
        connection.commit()


connection.commit()
# connection.close()
