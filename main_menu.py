import logging
import os
import re

import telegram
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, \
    ConversationHandler
from dotenv import load_dotenv

from keyboard_markups import main_menu_markup, start_stop_markup, categories_markup
from categories import categories, statistics

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
bot = telegram.Bot(TOKEN)


def start(update: Update, _: CallbackContext):
    reply_markup = main_menu_markup()
    update.message.reply_text('Виберіть варіант:', reply_markup=reply_markup)
    return 1


def start_over(update: Update, _: CallbackContext):
    message = 'Виберіть варіант:'
    reply_markup = main_menu_markup()
    query_edit_message(update, message, reply_markup=reply_markup)
    return 1


def categories_list(update, context: CallbackContext):
    reply_markup = categories_markup()
    message = 'Виберіть категорію:'
    query_edit_message(update, message, reply_markup=reply_markup)

    user_data = context.user_data
    user_data['categories'] = categories
    context.user_data['categories'] = user_data['categories']
    return 3


def send_statistics(update, context):
    period = statistics.get(update.callback_query.data)
    message = f'Витрати за {period}: <>'
    reply_markup = start_stop_markup()
    query_edit_message(update, message, reply_markup=reply_markup)
    return 4


def choose_category(update, context):
    key = update.callback_query.data
    current_category = context.user_data.get('categories').get(key)
    message = f"Введіть суму витрат для категорії '{current_category}' "
    query_edit_message(update, message)

    user_data = context.user_data
    user_data['category'] = key
    context.user_data['category'] = user_data['category']
    return 2


def check_user_input_expenses(update, context):
    key = context.user_data.get('category')
    current_category = context.user_data.get('categories').get(key)
    reply_markup = start_stop_markup()
    if isfloat(update.message.text) or update.message.text.isnumeric():
        expense = float(update.message.text)
        answer = f"Витрати {expense} грн збережено в категорії '{current_category}'."
        update.message.reply_text(answer, reply_markup=reply_markup)
        return 4
    else:
        answer = 'Будь ласка, введіть число'
        update.message.reply_text(answer)
        return 2


def isfloat(element):
    if re.match(r'^-?\d+(?:\.\d+)$', element) is None:
        return False
    return True


def stop(update: Update, _: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""

    chat_id = update.effective_chat.id
    bot.send_message(chat_id, text='Щасливо!')
    return ConversationHandler.END


def query_edit_message(update, message, **kwargs):
    query = update.callback_query
    query.answer()
    query.edit_message_text(message, **kwargs)


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [
                CallbackQueryHandler(categories_list, pattern='^1$'),
                CallbackQueryHandler(send_statistics, pattern='^2|3|4|5$'),

            ],
            2: [MessageHandler(Filters.regex(r'^.*$'), check_user_input_expenses, pass_user_data=True)
                ],
            3: [
                CallbackQueryHandler(choose_category, pattern=r'^\d$')
            ],
            4: [CallbackQueryHandler(start_over, pattern='^1$'),
                CallbackQueryHandler(stop, pattern='^2$'),

                ]

        },
        fallbacks=[CommandHandler('start', start)]
        ,
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('stop', stop))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
