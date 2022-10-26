from aiogram import executor
from handlers import client
from create_bot import dp
from data_bases import sqlite_db


async def on_startup(_):
    print('Бот запущено')
    sqlite_db.sql_start()


client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
