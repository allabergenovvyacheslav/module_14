# -*- coding: utf-8 -*-

from aiogram.dispatcher.filters.state import State, StatesGroup
from main_2 import *
from config_2 import *
from keyboards_2 import *
from database_2 import *
from main_2 import dp


# --------------ADMIN-------------------


@dp.message_handler(commands=['admin'])
async def admin(message):
    if message.from_user.id in admin:
        await message.answer('Панель администратора', reply_markup=admin_panel)
    else:
        await message.answer('Вы не являетесь администратором', reply_markup=None)


@dp.callback_query_handler(text='users')
async def users(call):
    await call.message.answer(show_users())
    await call.answer()


@dp.callback_query_handler(text='stat')
async def stat(call):
    await call.message.answer(show_stat())
    await call.answer()


class UserState(StatesGroup):
    id = State()


@dp.callback_query_handler(text='block')
async def block_user(call):
    await call.message.answer('Введите id пользователя')
    await UserState.id.set()
    await call.answer()


@dp.message_handler(state=UserState.id)
async def block_state(message, state):
    input_id = message.text
    add_to_block(input_id)
    await message.answer('Пользователь с указанным id был заблокирован')
    await state.finish()


class UserStateUn(StatesGroup):
    id = State()


@dp.callback_query_handler(text='block')
async def unblock_user(call):
    await call.message.answer('Введите id пользователя')
    await UserStateUn.id.set()
    await call.answer()


@dp.message_handler(state=UserStateUn.id)
async def block_state(message, state):
    input_id = message.text
    remove_block(input_id)
    await message.answer('Пользователь с указанным id был разблокирован')
    await state.finish()


# --------------END-ADMIN--------------