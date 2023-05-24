from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove


a1 = KeyboardButton('1')
a2 = KeyboardButton('2')
a3 = KeyboardButton('3')
a4 = KeyboardButton('4')
a5 = KeyboardButton('5')
a6 = KeyboardButton('6')
a7 = KeyboardButton('7')
a8 = KeyboardButton('8')
a9 = KeyboardButton('9')
a0 = KeyboardButton('0')


kb_client2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client2.add(a1).insert(a2).add(a3).insert(a4).add(a5).insert(a6).add(a7).insert(a8).add(a9).insert(a0)

