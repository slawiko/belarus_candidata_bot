#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

from candidata import data
from common import create_filter

CATEGORY_CHOOSING, CANDIDATE_CHOOSING, ANSWER = range(3)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def compose_message(entries):
    result = ''
    for entry in entries:
        result += '{}\n{}\n\n'.format(entry['description_ru'], entry['link'])
    return result


def start_handler(update, context):
    logger.info(context.user_data)
    greeting = "Про кого хотите узнать?"
    update.message.reply_text(greeting, reply_markup=data.get_candidates_keyboard())

    return CANDIDATE_CHOOSING


def candidate_handler(update, context):
    user_data = context.user_data
    user_data['candidate'] = update.message.text
    update.message.reply_text("А что?", reply_markup=data.get_categories_keyboard())

    return CATEGORY_CHOOSING


def category_handler(update, context):
    user_data = context.user_data
    user_data['category'] = update.message.text
    answer = compose_message(data.get(user_data['candidate'], user_data['category']))
    update.message.reply_text(answer, disable_web_page_preview=True)
    update.message.reply_text("Про кого еще хотите узнать?", reply_markup=data.get_candidates_keyboard())

    return CANDIDATE_CHOOSING


def wrong_handler(update, context):
    update.message.reply_text("Пожалуйста, используйте клавиатуру")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    TOKEN = ""

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            CANDIDATE_CHOOSING: [MessageHandler(create_filter(data.names), candidate_handler)],
            CATEGORY_CHOOSING: [MessageHandler(create_filter(data.categories), category_handler)],
        },
        fallbacks=[MessageHandler(Filters.text, wrong_handler)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
