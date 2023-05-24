from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove


a1 = KeyboardButton('Январь')
a2 = KeyboardButton('Февраль')
a3 = KeyboardButton('Март')
a4 = KeyboardButton('Апрель')
a5 = KeyboardButton('Май')
a6 = KeyboardButton('Июнь')
a7 = KeyboardButton('Июль')
a8 = KeyboardButton('Август')
a9 = KeyboardButton('Сентябрь')
a0 = KeyboardButton('Октябрь')
a10 = KeyboardButton('Ноябрь')
a11 = KeyboardButton('декабрь')

kb_client4 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client4.add(a1).insert(a2).add(a3).insert(a4).add(a5).insert(a6).add(a7).insert(a8).add(a9).insert(a0).add(a10).insert(a11)

