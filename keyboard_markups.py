from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from categories import Categories


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
    categories = Categories().all_categories
    for id_number, category_name in categories.items():
        keyboard.append([InlineKeyboardButton(category_name['name_ua'], callback_data=str(id_number))])
    return InlineKeyboardMarkup(keyboard)
