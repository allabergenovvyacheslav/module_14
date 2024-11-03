# -*- coding: utf-8 -*-

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config_2 import *
from keyboards_2 import *
import texts_2
from admin_2 import *
from database_2 import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())

# --------------MAIN-------------------

@dp.message_handler(commands=['start'])
async def start(message):
    with open('files/troniy_zal.png', 'rb') as img:
        await message.answer_photo(img, f'Добро пожаловать, {message.from_user.full_name}!\n\n'
                                   + texts_2.start, reply_markup=start_kb)


@dp.message_handler(text="О компании Мир паркета")
async def inform(message):
    with open('files/privet.png', 'rb') as img:
        await message.answer_photo(img, texts_2.about, reply_markup=start_kb)


@dp.message_handler(text="Прайс-лист на паркет")
async def price_parquet(message):
    await message.answer("Выберите позицию из прайса", reply_markup=catalog_kb)


@dp.message_handler(text="Прайс-лист на услуги")
async def price_works(message):
    await message.answer("Основные этапы комплекса работ", reply_markup=works_kb)


@dp.callback_query_handler(text="fanera_works")
async def fanera_work(call):
    with open(f"files/fanera.jpg", "rb") as img:
        await call.message.answer_photo(img, texts_2.fanera_works, reply_markup=order_work)
    await call.answer()


@dp.callback_query_handler(text="parquet_works")
async def parquet_work(call):
    with open(f"files/parquet_works.jpg", "rb") as img:
        await call.message.answer_photo(img, texts_2.parquet_works, reply_markup=order_work)
    await call.answer()


@dp.callback_query_handler(text="otdelka_works")
async def otdelka_work(call):
    with open(f"files/otdelka_works.jpg", "rb") as img:
        await call.message.answer_photo(img, texts_2.otdelka_works, reply_markup=order_work)
    await call.answer()


@dp.message_handler(text='Наши работы')
async def show_work(message):
    for x in range(1, 14):
        with open(f'files_2/{x}.jpg', 'rb') as img:
            await message.answer_photo(img, texts_2.show_work, reply_markup=start_kb)


@dp.callback_query_handler(text="parquet_flooring_RS")
async def buy_parquet_flooring_RS(call):
    with open('files/radial.jpeg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.parquet_flooring_RS, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="large_format_parquet_RS")
async def buy_large_format_parquet_RS(call):
    with open('files/radial.jpeg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.large_format_parquet_RS, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="parquet_flooring_S")
async def buy_parquet_flooring_S(call):
    with open('files/select.jpeg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.parquet_flooring_S, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="large_format_parquet_S")
async def buy_large_format_parquet_S(call):
    with open('files/large_S.jpg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.large_format_parquet_S, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="solid_wood_parquet_S")
async def buy_solid_wood_parquet_S(call):
    with open('files/solid_S.jpg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.solid_wood_parquet_S, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="parquet_flooring_N")
async def buy_parquet_flooring_N(call):
    with open('files/natur.jpeg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.parquet_flooring_N, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="large_format_parquet_N")
async def buy_large_format_parquet_N(call):
    with open('files/large_N.jpg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.large_format_parquet_N, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="solid_wood_parquet_N")
async def buy_solid_wood_parquet_N(call):
    with open('files/solid_N.jpg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.solid_wood_parquet_N, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="parquet_flooring_R")
async def buy_parquet_flooring_R(call):
    with open('files/rustic.jpeg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.parquet_flooring_R, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="large_format_parquet_R")
async def buy_large_format_parquet_R(call):
    with open('files/large_Rust.jpg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.large_format_parquet_R, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="solid_wood_parquet_R")
async def buy_solid_wood_parquet_R(call):
    with open('files/solid_Rust.jpg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.solid_wood_parquet_R, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="oter")
async def buy_other(call):
    with open('files/other.jpg', 'rb') as img:
        await call.message.answer_photo(img, texts_2.oter, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='back_to_catalog')
async def cmd_back_price(call):
    await call.message.answer("Выберите позицию из прайса", reply_markup=catalog_kb)
    await call.answer()


@dp.callback_query_handler(text='back_to_works')
async def cmd_back_work(call):
    await call.message.answer("Основные этапы комплекса работ", reply_markup=works_kb)
    await call.answer()

# ------------------END-MAIN----------------------


if __name__ == '__main__':
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    executor.start_polling(dp, skip_updates=True)
    connection.commit()
    connection.close()
