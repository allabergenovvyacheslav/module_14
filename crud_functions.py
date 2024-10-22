# -*- coding: utf-8 -*-

# Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:

# initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса.

# Эта таблица должна содержать следующие поля:
# id - целое число, первичный ключ
# username - текст (не пустой)
# email - текст (не пустой)
# age - целое число (не пустой)
# balance - целое число (не пустой)

# add_user(username, email, age), которая принимает: имя пользователя, почту и возраст.
# Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными.
# Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте
# SQL запрос.

# is_included(username) принимает имя пользователя и возвращает True, если такой пользователь
# есть в таблице Users, в противном случае False. Для получения записей используйте SQL запрос.

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


def add_user(username, email, age):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)",
                   (username, email, age, 1000))
    connection.commit()


def is_included(username):
    user = cursor.execute('SELECT * FROM Users Where username = ?',
                          (username,))
    if user.fetchone() is None:
        return False
    else:
        return True


connection.commit()
# connection.close()
