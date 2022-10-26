from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from create_bot import bot, dp
from keyboards.client_kb import keyboard_goods, keyboard_general, keyboard_statistics
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_bases.sqlite_db import sql_add, sql_this_month, sql_last_month, sql_enter_period

ID = None


class FsmGoods(StatesGroup):
    """Клас для машини стану збереження витрат"""
    goods = State()
    sum = State()


class FsmStatistic(StatesGroup):
    """Клас для машини стану отримання статистики за витратами за заданий період"""
    period = State()


async def command_start(message: Message):
    """Команда для старту"""
    await bot.send_message(message.from_user.id, "Hi! Choose: add expenses or view statistics",
                           reply_markup=keyboard_general)


async def add_expenses_start(message: types.Message):
    """Збереження витрат: отримуємо ID, запускаємо машину стану"""
    global ID
    ID = message.from_user.id
    await FsmGoods.goods.set()
    await message.answer("Choose the category", reply_markup=keyboard_goods)
    await message.delete()


async def add_expenses_cancel(message: types.Message, state: FSMContext):
    """Збереження витрат: переривання збереження, вихід зі стану"""
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer("Choose: add expenses or view statistics",
                             reply_markup=keyboard_general)


async def add_expenses_category(message: types.Message, state: FSMContext):
    """Збереження витрат: фіксуємо категорію, id та дату"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["id"] = message.from_user.id
            data["goods"] = message.get_command()
            data["date"] = message.date.date()
        await FsmGoods.next()
        await message.reply('Enter sum')


async def add_expenses_sum(message: types.Message, state: FSMContext):
    """Збереження витрат: зберігаємо суму, закінчуємо машину стану"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['sum'] = int(message.text)
        await sql_add(state)
        await message.answer('Saved', reply_markup=keyboard_general)
        await state.finish()


async def view_statistics(message: types.Message):
    """Клавіатура статистики по витратах"""
    await message.answer("Choose the period", reply_markup=keyboard_statistics)


async def view_statistics_this_month(message: types.Message):
    """Статистика по витратах: за цей місяць"""
    id = message.from_user.id
    await sql_this_month(id)


async def view_statistics_last_month(message: types.Message):
    """Статистика по витратах: за минулий місяць"""
    id = message.from_user.id
    await sql_last_month(id)


async def add_period_start(message: types.Message):
    """Отримуємо період: отримуємо ID, запускаємо машину стану"""
    global ID
    ID = message.from_user.id
    await FsmStatistic.period.set()
    await message.answer("Enter the period like '1.10.22 - 15.10.22'")


async def add_period_finish(message: types.Message, state: FSMContext):
    """Отримуємо період: опрацьовуємо дати, закінчуємо машину стану"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["id"] = message.from_user.id
            data["period"] = message.text
        await sql_enter_period(data)
        await state.finish()


def register_handlers_client(dp: Dispatcher):
    """Реєстрація хендлерів"""
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(add_expenses_start, commands=["Add_expenses"], state=None)
    dp.register_message_handler(add_expenses_cancel, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(add_expenses_category,
                                commands=["Everyday_goods", "Eat_out", "Medicine", "Travel", "Rest", "Clothing", "Pet",
                                          "Vehicle", "Transport", "Technique", "Repair", "Book"], state=FsmGoods.goods)
    dp.register_message_handler(add_expenses_sum, state=FsmGoods.sum)
    dp.register_message_handler(add_expenses_cancel, state="*", commands="cancel")
    dp.register_message_handler(view_statistics, commands=["Statistics"])
    dp.register_message_handler(view_statistics_this_month, commands=["This_month"])
    dp.register_message_handler(view_statistics_last_month, commands=["Last_month"])
    dp.register_message_handler(add_period_start, commands=["Enter_period"], state=None)
    dp.register_message_handler(add_period_finish, state=FsmStatistic.period)
