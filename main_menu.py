import logging
from categories import categories, statistics
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, \
    ConversationHandler

import os
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
bot = telegram.Bot(TOKEN)


def start(update: Update, _: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Категорії витрат", callback_data='1'),
        ],
        [InlineKeyboardButton("Витрати за день", callback_data='2'),
         InlineKeyboardButton("Витрати за тиждень", callback_data='week')],
        [InlineKeyboardButton("Витрати за місяць", callback_data='month'),
         InlineKeyboardButton("Витрати за рік", callback_data='year')],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Виберіть варіант:', reply_markup=reply_markup)
    return 1


def start_over(update: Update, _: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Категорії витрат", callback_data='1'),
        ],
        [InlineKeyboardButton("Витрати за день", callback_data='2'),
         InlineKeyboardButton("Витрати за тиждень", callback_data='3')],
        [InlineKeyboardButton("Витрати за місяць", callback_data='4'),
         InlineKeyboardButton("Витрати за рік", callback_data='5')],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Виберіть варіант:', reply_markup=reply_markup)
    return 1


def categories_list(update, context: CallbackContext):
    keyboard = []
    query = update.callback_query
    query.answer()
    for number, category_name in categories.items():
        keyboard.append([InlineKeyboardButton(category_name, callback_data=number)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Виберіть категорію:', reply_markup=reply_markup)

    user_data = context.user_data
    user_data['categories'] = categories
    context.user_data['categories'] = user_data['categories']
    return 3


def send_statistics(update, context):
    query = update.callback_query
    query.answer()
    period = statistics.get(update.callback_query.data)
    query.edit_message_text(f'Витрати за {period}: ...')
    return 1


def choose_category(update, context):
    query = update.callback_query
    query.answer()
    key = update.callback_query.data
    current_category = context.user_data.get('categories').get(key)
    query.edit_message_text(f"Введіть суму витрат для категорії '{current_category}' ")

    user_data = context.user_data
    user_data['category'] = key
    context.user_data['category'] = user_data['category']
    return 2


def save_expense(update, context):
    key = context.user_data.get('category')
    current_category = context.user_data.get('categories').get(key)
    try:
        expense = float(update.message.text)
    except ValueError:
        answer = 'Будь ласка, введіть число'
    else:
        answer = f"Витрати {expense} грн збережено в категорії '{current_category}'."
    update.message.reply_text(answer)
    return 4


def stop(update: Update, _: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    update.message.reply_text('Гарного дня.')
    return ConversationHandler.END


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [
                CallbackQueryHandler(categories_list, pattern='^' + '1' + '$'),
                CallbackQueryHandler(send_statistics, pattern='^' + '2|3|4|5' + '$'),
            ],
            2: [MessageHandler(Filters.text, save_expense, pass_user_data=True)
                ],
            3: [
                CallbackQueryHandler(choose_category, pattern='^' + '\d' + '$')
            ],
            4: [CallbackQueryHandler(start_over)
                ],
        },
        fallbacks=[CommandHandler('start', start)]
        ,
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('stop', stop))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
