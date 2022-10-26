from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки клавіатури категорій витрат
button1 = KeyboardButton("/Everyday_goods")
button2 = KeyboardButton("/Eat_out")
button3 = KeyboardButton("/Medicine")
button4 = KeyboardButton("/Travel")
button5 = KeyboardButton("/Rest")
button6 = KeyboardButton("/Clothing")
button7 = KeyboardButton("/Pet")
button8 = KeyboardButton("/Vehicle")
button9 = KeyboardButton("/Transport")
button10 = KeyboardButton("/Technique")
button11 = KeyboardButton("/Repair")
button12 = KeyboardButton("/Book")

# Клавіатура категорій витрат
keyboard_goods = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_goods.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10,
                   button11, button12)


# Кнопки клавіатури загальної категорії
general_b1 = KeyboardButton("/Add_expenses")
general_b2 = KeyboardButton("/Statistics")

# Клавіатура загальної категорії
keyboard_general = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_general.add(general_b1, general_b2)


# Кнопки клавіатури статистики
statistics_b1 = KeyboardButton("/This_month")
statistics_b2 = KeyboardButton("/Last_month")
statistics_b3 = KeyboardButton("/Enter_period")

# Клавіатура статистики
keyboard_statistics = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_statistics.add(statistics_b1, statistics_b2, statistics_b3).add(general_b1)


