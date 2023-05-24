from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove


b1 = KeyboardButton('/План')
b2 = KeyboardButton('/Отправить_Отчет')
b3 = KeyboardButton('/Отчет_дня')
b4 = KeyboardButton('/Отчет_месяца')
b5 =KeyboardButton ('/Дата_визуализация')
b6 = KeyboardButton ('/Admin')
b7 = KeyboardButton('/Отчет_ваш')
b8 = KeyboardButton('/Лучшее_сотрудники_месяца')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1).insert(b2).add(b3).insert(b4).add(b5).insert(b6).add(b7).insert(b8)


