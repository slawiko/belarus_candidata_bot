#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

from telegram import ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

from src.candidata import data
from src.common import create_filter
from src.by import commands, states

CATEGORY_CHOOSING, CANDIDATE_CHOOSING, ANSWER = range(3)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def compose_message(entries):
    result = ''
    for entry in entries:
        result += '{}\n{}\n\n'.format(entry['description'], entry['link'])
    return result


def start_handler(update, context):
    logger.info('User %s run %s command', update.effective_user.id, '/start')
    update.message.reply_text(commands.get('start'), reply_markup=data.get_candidates_keyboard())

    return CANDIDATE_CHOOSING


def contribute_handler(update, context):
    logger.info('User %s run %s command', update.effective_user.id, '/contribute')
    update.message.reply_text(commands.get('contribute'))


def candidate_handler(update, context):
    user_data = context.user_data
    user_data['candidate'] = update.message.text
    logger.info('User %s choose %s candidate', update.effective_user.id, user_data['candidate'])
    update.message.reply_text(states.get('candidate'), reply_markup=data.get_categories_keyboard(user_data['candidate']))

    return CATEGORY_CHOOSING


def category_handler(update, context):
    user_data = context.user_data
    user_data['category'] = update.message.text
    logger.info('User %s choose %s category', update.effective_user.id, user_data['category'])
    answer = compose_message(data.get(user_data['candidate'], user_data['category']))
    update.message.reply_text(answer, disable_web_page_preview=True)
    update.message.reply_text(states.get('category'), reply_markup=ReplyKeyboardRemove())

    user_data.clear()
    return ConversationHandler.END


def wrong_handler(update, context):
    logger.info('User %s sent unrecognized text %s', update.effective_user.id, update.message.text)
    update.message.reply_text(states.get('wrong'), reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(update, context):
    logger.error('Update "%s" caused error "%s"', update, context.error)
    return ConversationHandler.END


def timeout_handler(update, context):
    user_data = context.user_data
    user_data.clear()
    logger.info('User %s received timeout', update.effective_user.id)
    update.message.reply_text(states.get('timeout'), reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main(token):
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        allow_reentry=True,
        conversation_timeout=300,
        entry_points=[CommandHandler('start', start_handler),
                      CommandHandler('contribute', contribute_handler)],
        states={
            CANDIDATE_CHOOSING: [MessageHandler(create_filter(data.names), candidate_handler)],
            CATEGORY_CHOOSING: [MessageHandler(create_filter(data.categories), category_handler)],
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.all, timeout_handler)],
        },
        fallbacks=[MessageHandler(Filters.all, wrong_handler)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    TOKEN = sys.argv[1]
    main(TOKEN)
