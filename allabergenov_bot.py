# -*- coding: utf-8 -*-


import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from crud_functions import *


api = ''
bot = Bot(token=api, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

keyboard_1 = ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder='Введите данные здесь')
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')
button_3_1 = KeyboardButton(text='Регистрация')
keyboard_1.add(button_1, button_2)
keyboard_1.add(button_3, button_3_1)

keyboard_2: InlineKeyboardMarkup = InlineKeyboardMarkup()
button_4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_5 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
keyboard_2.add(button_4)
keyboard_2.add(button_5)

keyboard_3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying'),
         InlineKeyboardButton(text='Product2', callback_data='product_buying'),
         InlineKeyboardButton(text='Product3', callback_data='product_buying'),
         InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ],
    resize_keyboard=True
)

keyboards_4: InlineKeyboardMarkup = InlineKeyboardMarkup()
button_6 = InlineKeyboardButton(text='мужчина', callback_data='man')
button_7 = InlineKeyboardButton(text='женщина', callback_data='woman')
keyboards_4.add(button_6, button_7)

keyboard_5: InlineKeyboardMarkup = InlineKeyboardMarkup()
button_8 = InlineKeyboardButton(text='Все верно', callback_data='correct')
button_9 = InlineKeyboardButton(text='Редактировать', callback_data='incorrect')
keyboard_5.add(button_8, button_9)


#-------------ADMIN---------------
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


#-----------------END-ADMIN---------------

#--------------------MAIN-----------------


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()
    check_state = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=keyboard_1)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
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
    await call.message.answer(
        'для <u>мужчин:</u> 10 <i>х</i> вес(кг) <i>+</i> 6,25 <i>х</i> рост(см) – 5 <i>х</i> возраст(г) <i>+</i> 5;\n\n'
        'для <u>женщин:</u> 10 <i>х</i> вес(кг) <i>+</i> 6,25 <i>х</i> рост(см) – 5 <i>х</i> возраст(г) <i>-</i> 161'
    )
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_gender(call):
    await call.message.answer('Выберите свой пол: муж/жен', reply_markup=keyboards_4)
    await UserState.gender.set()


@dp.callback_query_handler(state=UserState.gender)
async def set_age1(call, state):
    await state.update_data(gender=call.data)
    await call.message.answer("Введите свой возраст:")
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


@dp.message_handler(state=UserState.weight)
async def check_state(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    await message.answer(f"Подтвердите Ваши данные:\n"
                         f"Вы {message.from_user.full_name},\n"
                         f"Ваш пол {data['gender']},\n"
                         f"Вам {data['age']} лет,\n"
                         f"Ваш рост {data['growth']} см,\n"
                         f"Ваш вес {data['weight']} кг",
                         reply_markup=keyboard_5)
    await UserState.check_state.set()


@dp.callback_query_handler(state=UserState.check_state)
async def correct_data(call, state):
    await state.update_data(check_state=call.data)
    call.data = await state.get_data()
    if call.data['check_state'] == 'correct':
        await call.answer('Данные приняты!')
        await call.message.answer(f'Для результата нажмите команду:\n /return')
    else:
        await call.message.answer('Выберите свой пол: муж/жен', reply_markup=keyboards_4)
        await UserState.gender.set()


@dp.message_handler(commands=['return'])
async def return_data(message, state):
    global res_for_woman, res_for_man
    data = await state.get_data()
    if data['gender'] == 'woman':
        res_for_woman = (
                    10 * data['weight']
                    + 6.25 * data['growth']
                    - 5 * data['age']
                    - 161
            )
    await message.answer(f'Ваша норма суточная норма калорий\n {res_for_woman} ккал')
    if data['gender'] == 'man':
        res_for_man = (
                10 * data['weight']
                + 6.25 * data['growth']
                - 5 * data['age']
                + 5
        )
    await message.answer(f'Ваша норма суточная норма калорий\n {res_for_man} ккал')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
