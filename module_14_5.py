# -*- coding: utf-8 -*-


# Изменения в Telegram-бот:

# Кнопки главного меню дополните кнопкой "Регистрация".

# Напишите новый класс состояний RegistrationState с следующими объектами класса
# State: username, email, age, balance(по умолчанию 1000).
# Создайте цепочку изменений состояний RegistrationState.
#
# Фукнции цепочки состояний RegistrationState:
#
# sing_up(message):
#
# Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
# Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя
# (только латинский алфавит):".
# После ожидать ввода возраста в атрибут RegistrationState.username при помощи метода set.
#
# set_username(message, state):
#
# Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
# Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии
# username на message.text.
# Далее выводится сообщение "Введите свой email:" и принимается новое состояние
# RegistrationState.email.
# Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует,
# введите другое имя" и запрашивать новое состояние для RegistrationState.username.
#
# set_email(message, state):
#
# Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
# Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
# Далее выводить сообщение "Введите свой возраст:":
# После ожидать ввода возраста в атрибут RegistrationState.age.
#
# set_age(message, state):
#
# Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
# Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
# Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users
# при помощи ранее написанной crud-функции add_user.#
# В конце завершать приём состояний при помощи метода finish().

# Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего
# вывода в чате Telegram-бота.


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import crud_functions
from crud_functions import *


api = '7817004865:AAFBqVj3Xa3maRLafdwpfAYqoBnVr0IBUdw'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


keyboard_3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying'),
         InlineKeyboardButton(text='Product2', callback_data='product_buying'),
         InlineKeyboardButton(text='Product3', callback_data='product_buying'),
         InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ],
    resize_keyboard=True
)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer('Вы зарегистрировались, для продолжения введите /start')
    await state.finish()


class UserState(StatesGroup):
    gender_man = State()
    gender_woman = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    button_1 = KeyboardButton(text='Рассчитать')
    button_2 = KeyboardButton(text='Информация')
    button_3 = KeyboardButton(text='Купить')
    button_3_1 = KeyboardButton(text='Регистрация')
    keyboard_1 = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder='Введите данные здесь')
    keyboard_1.add(button_1, button_2)
    keyboard_1.add(button_3, button_3_1)
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=keyboard_1)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    button_4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
    button_5 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
    keyboard_2: InlineKeyboardMarkup = InlineKeyboardMarkup()
    keyboard_2.add(button_4)
    keyboard_2.add(button_5)
    await message.answer('Выберите опцию:', reply_markup=keyboard_2)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Этот бот призван помочь вам не перебрать лишних калорий '
                         'и приобрести полезные продукты.')


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    all_product = get_all_products()
    for x in range(1, 5):
        await message.answer(f'{all_product[x][1]} {all_product[x][2]} {all_product[x][3]}')
        with open(f'images/{x}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=keyboard_3)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5; '
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_gender(call):
    button_6 = InlineKeyboardButton(text='man', callback_data='gender_man')
    button_7 = InlineKeyboardButton(text='woman', callback_data='gender_woman')
    keyboards_4: InlineKeyboardMarkup = InlineKeyboardMarkup()
    keyboards_4.add(button_6, button_7)
    await call.message.answer('Выберите свой пол: man/woman', reply_markup=keyboards_4)
    await UserState.gender_man.set()
    await UserState.gender_woman.set()


@dp.callback_query_handler(state=UserState.gender_man)
async def set_age(call, state):
    await state.update_data(gender_man=call.message)
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.callback_query_handler(state=UserState.gender_woman)
async def set_age(call, state):
    await state.update_data(gender_woman=call.message)
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост в см:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес в кг:')
    await UserState.weight.set()


@dp.callback_query_handler(state=UserState.gender_man)
async def send_calories_man(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    res1 = (
                10 * data['weight']
                + 6.25 * data['growth']
                - 5 * data['age']
                + 5
        )
    await message.answer(f'Ваша норма калорий {res1}')
    await state.finish()


@dp.callback_query_handler(state=UserState.gender_woman)
async def send_calories_man(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    res2 = (
                10 * data['weight']
                + 6.25 * data['growth']
                - 5 * data['age']
                - 161
        )
    await message.answer(f'Ваша норма калорий {res2}')
    await state.finish()


# @dp.message_handler(state=UserState.weight)
# async def send_calories(message, state):
#     await state.update_data(weight=int(message.text))
#     data = await state.get_data()
#     if data['gender'] == 'woman':
#         res_for_woman = (
#                 10 * data['weight']
#                 + 6.25 * data['growth']
#                 - 5 * data['age']
#                 - 161
#         )
#         await message.answer(f'Ваша норма калорий {res_for_woman}')
#     if data['gender'] == 'man':
#         res_for_man = (
#                 10 * data['weight']
#                 + 6.25 * data['growth']
#                 - 5 * data['age']
#                 + 5
#         )
#         await message.answer(f'Ваша норма калорий {res_for_man}')
#     await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)