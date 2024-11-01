#  Домашнее задание по теме "Доработка бота"
# Цель: подготовить Telegram-бота для взаимодействия с базой данных.
#
# Задача "Витамины для всех!":


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = "здесь секретный код"

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button11 = KeyboardButton(text="Расчитать")
button12 = KeyboardButton(text="Информация")
button13 = KeyboardButton(text="Купить")
kb.row(button11, button12)
kb.add(button13)

kb2 = InlineKeyboardMarkup()
button21 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button22 = KeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2.row(button21, button22)

kb3 = InlineKeyboardMarkup()
button31 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button32 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button33 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button34 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb3.row(button31, button32, button33, button34)



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=["Расчитать"])
async def mai_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)

@dp.message_handler(text=["Купить"])
async def get_buying_list(message):
    for number in range(1, 5):
        await message.answer(f"Название: Product{number} | Описание: Для 'Product{number} | Цена: {number * 100}")
        with open(f'files/vit_{number}.jpg', 'rb') as img:
            await message.answer_photo(img, "*** Витамины, доступные для всех! Только у нас и для Вас! ***")
            await message.answer("Выберите продукт для покупки:", reply_markup=kb3)
@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await (UserState.growth.set())


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.callback_query_handler(text=["formulas"])
async def get_formulas(call):
    await call.message.answer(f"10 x вес(кг) + 6,25 x рост(см) + 5 x возраст(лет) - 161")



@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(
        f"Ваша норма калорий:{10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) - 161}")
    await state.finish()


@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью. Нажмите кнопку 'Расчитать'", reply_markup=kb)


@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)