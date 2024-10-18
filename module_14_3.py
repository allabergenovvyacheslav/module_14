# -*- coding: utf-8 -*-

# Задача "Витамины для всех!":
#
# Подготовка:
#
# Подготовьте Telegram-бота из последнего домашнего задания 13 моудля сохранив код с ним в
# файл module_14_3.py.
#
# Дополните ранее написанный код для Telegram-бота:
#
# Создайте и дополните клавиатуры:
#
# В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
#
# Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4".
# У всех кнопок назначьте callback_data="product_buying"
#
# Создайте хэндлеры и функции к ним:
#
# Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию
# get_buying_list(message).
#
# Функция get_buying_list должна выводить надписи 'Название: Product<number> |
# Описание: описание <number> | Цена: <number * 100>' 4 раза. После каждой надписи выводите
# картинки к продуктам.
#
# В конце выведите ранее созданное Inline меню с надписью "Выберите продукт для покупки:".
#
# Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию
# send_confirm_message(call). Функция send_confirm_message, присылает сообщение
# "Вы успешно приобрели продукт!"


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
    button_3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
    button_4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
    keyboard_2: InlineKeyboardMarkup = InlineKeyboardMarkup()
    keyboard_2.add(button_3)
    keyboard_2.add(button_4)
    await message.answer('Выберите опцию:', reply_markup=keyboard_2)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer(
        'Этот бот помогает рассчитать сколько вам необходимо потреблять ежедневно калорий.'
    )


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for x in range(1, 5):
        await message.answer(f'Product{x} | Описание{x} | Цена: {x*100}')
        with open(f'images/1.jpg', 'rb') as img:
            await message.answer_foto(img)
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
    button_9 = InlineKeyboardButton(text='men', callback_data='gender')
    button_10 = InlineKeyboardButton(text='women', callback_data='gender')
    keyboards_4: InlineKeyboardMarkup = InlineKeyboardMarkup()
    keyboards_4.add(button_9)
    keyboards_4.add(button_10)
    await call.message.answer('Назовите свой пол: men/women', reply_markup=keyboards_4)
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    await state.update_data(gender=message.text.lower())
    await message.answer('Введите свой возраст:')
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
    if data['gender'] == 'women':
        res_for_women = (
                10 * data['weight']
                + 6.25 * data['growth']
                - 5 * data['age']
                - 161
        )
        await message.answer(f'Ваша норма калорий {res_for_women}')
    if data['gender'] == 'men':
        res_for_men = (
                10 * data['weight']
                + 6.25 * data['growth']
                - 5 * data['age']
                + 5
        )
        await message.answer(f'Ваша норма калорий {res_for_men}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
