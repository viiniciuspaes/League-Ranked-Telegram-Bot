import telegram
import logging
import constants as con
from telegram.ext import Updater


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

bot = telegram.Bot(token=con.bot_token)
updater = Updater(token=con.bot_token, use_context=True)

print(bot.get_me())
