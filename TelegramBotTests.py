from telegram.ext import Updater, CommandHandler, PollHandler
from telegram.ext.dispatcher import run_async
import requests
import re



def main():
    updater = Updater('2116134001:AAHl_y9JAdFs0-SKuzVZICONmJ-BHpZjZvI', use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler('Quiz', help_commandar_handler))
    # Message
    dp.add_handler(CommandHandler('Filters.txt', main_handler))
    # Quiz handler
    dp.add_handler(PollHandler(poll_handler, pass_chat_data=True, pass_user_data=True))

    # start
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()