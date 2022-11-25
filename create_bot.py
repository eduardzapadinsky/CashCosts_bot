import os
from aiogram import Bot, Dispatcher
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


bot = Bot(token=config.TOKEN) # using for heroku
# bot = Bot(token=os.getenv('TOKEN')) # using for localhost
dp = Dispatcher(bot, storage=storage)
