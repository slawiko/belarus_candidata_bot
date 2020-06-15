from telegram import ReplyKeyboardMarkup
from telegram.ext.filters import Filters


def create_markup(keys):
    keyboard = []

    for i in range(0, len(keys), 2):
        keyboard.append(keys[i:i + 2])

    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)


def create_filter(keys):
    return Filters.regex('^{}$'.format('|'.join(keys)))
