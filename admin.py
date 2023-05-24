from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
API_TOKEN = '5527521010:AAGkz20GIqmvoQigQNQzQ-u9ZLNUL139huE'
import aiogram.utils.markdown as md
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
from aiogram.dispatcher import filters


ad1 = KeyboardButton('/План_месяц')
ad2= KeyboardButton('/Delete_all')
ad3= KeyboardButton('/Email')
ad4 = KeyboardButton('/Главное')
kb_client3 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client3.add(ad1).insert(ad2).add(ad3).insert(ad4)


