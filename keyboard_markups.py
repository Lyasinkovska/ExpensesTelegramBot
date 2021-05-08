from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from categories import categories


def main_menu_markup():
    keyboard = [
        [
            InlineKeyboardButton("Категорії витрат", callback_data='1'),
        ],
        [InlineKeyboardButton("Витрати за день", callback_data='2'),
         InlineKeyboardButton("Витрати за тиждень", callback_data='3')],
        [InlineKeyboardButton("Витрати за місяць", callback_data='4'),
         InlineKeyboardButton("Витрати за рік", callback_data='5')],

    ]
    return InlineKeyboardMarkup(keyboard)


def start_stop_markup():
    keyboard = [
        [
            InlineKeyboardButton("На головну", callback_data='1'),
            InlineKeyboardButton("Завершити", callback_data='2')
        ],

    ]
    return InlineKeyboardMarkup(keyboard)


def categories_markup():
    keyboard = []
    for number, category_name in categories.items():
        keyboard.append([InlineKeyboardButton(category_name, callback_data=number)])
    return InlineKeyboardMarkup(keyboard)


