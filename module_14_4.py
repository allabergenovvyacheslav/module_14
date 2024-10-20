# -*- coding: utf-8 -*-




from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    button_1 = KeyboardButton(text='Рассчитать')
    button_2 = KeyboardButton(text='Информация')
    button_3 = KeyboardButton(text='Купить')
    keyboard_1 = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder='Введите данные здесь')
    keyboard_1.add(button_1, button_2)
    keyboard_1.add(button_3)
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=keyboard_1)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    button_4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
    button_5 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
    keyboard_2: InlineKeyboardMarkup = InlineKeyboardMarkup()
    keyboard_2.add(button_4)
    keyboard_2.add(button_5)
    await message.answer('Выберите опцию:', reply_markup=keyboard_2)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    all_product = get_all_products()
    for i in range(len(all_product)):
        await message.answer(f'{all_product[i][1]} | {all_product[i][2]} | {all_product[i*100][3]}')
        with open(f'images/{i}.jpg', 'rb') as img:
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
    button_6 = InlineKeyboardButton(text='man', callback_data='gender')
    button_7 = InlineKeyboardButton(text='woman', callback_data='gender')
    keyboards_4: InlineKeyboardMarkup = InlineKeyboardMarkup()
    keyboards_4.add(button_6, button_7)
    await call.message.answer('Выберите свой пол: man/woman', reply_markup=keyboards_4)
    await UserState.gender.set()


@dp.callback_query_handler(state=UserState.gender)
async def set_age(call, state):
    await state.update_data(gender=call.message.text)
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


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    if data['gender'] == 'woman':
        res_for_woman = (
                10 * data['weight']
                + 6.25 * data['growth']
                - 5 * data['age']
                - 161
        )
        await message.answer(f'Ваша норма калорий {res_for_woman}')
    if data['gender'] == 'man':
        res_for_man = (
                10 * data['weight']
                + 6.25 * data['growth']
                - 5 * data['age']
                + 5
        )
        await message.answer(f'Ваша норма калорий {res_for_man}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)