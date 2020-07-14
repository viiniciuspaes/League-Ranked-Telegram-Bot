import telegram
import logging
import riot_api
import constants as con
from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

__version__ = "1.0"

def help_msg(updater, context):
    msg = "Hi Summoner! Some usefull information on how to talk to me\n"\
        "/start to know more about me\n"\
        "/summoner <Summoner Name> to get account info\n"\
        "/Mastery <Summoner Name> to know How many champions you have mastery\n"\
        "/lol <Summoner Name> to get some of your League of legends ranked stats\n"\
        "/tft <Summoner Name> to get some of your Teamfight Tactics ranked stats(Not yet available)"
    updater.message.reply_text(msg)

def start_msg(updater, conxtext):
    msg = "So.. What can I do?\n"\
        "League ranked info, I`m a bot that allows you to check "\
        "some basic ranked info from Riot runneterra based games: \n"\
        "\n- League of Legends"\
        "\n- Teamfight Tactics(Comming soon)"\
        "\n- Legends of Runeterra(Comming soon)"\
        "\n- Valorant(Comming soon)"\
        "\n- You will be able to verify: "\
        "\n- wins"\
        "\n- Looses"\
        "\n- Win rate"\
        "\n- Tier"\
        "\n- Rank"\
        "\n- PDL"\
        "\n- Total valid matches"\
        "\n\nAll of this with a simple chat message. Talk to me\n"\
        f"\nVersion: {__version__}\n"\
        "\nI was created by Vinicius \"Torack\" Paes, "\
        "as a open source project."\
        "\nCheck on:\n https://github.com/viiniciuspaes/League-Ranked-Telegram-Bot"

    updater.message.reply_text(msg)


def update_user(updater, context):
    try:
        account_info = riot_api.update_account_secure_info("".join(context.args))
        msg = "Summoner Name: {}\n"\
            "Summoner Level: {}\n"\
            "Last Update: {}\n"\
            "Acount id {}".format(account_info["name"],
                            account_info["summoner_level"],
                            account_info["revision"],
                            account_info["id"])
        updater.message.reply_text(msg) 

    except KeyError:
        updater.message.reply_text("ERROR: Invalid Summoner")
    
   
def mastered_champions(updater, context):
    try:
        account = riot_api.update_account_secure_info("".join(context.args))
        number = riot_api.get_mastered_lol_champions(account["id"])
        updater.message.reply_text("Account {} has {} mastered champions"\
        .format(account["name"], number))

    except KeyError:
        updater.message.reply_text("ERROR: Invalid Summoner")


def ranked_lol_info(updater,  context):
    try:
        account = riot_api.update_account_secure_info("".join(context.args))
        ranked_queue = riot_api.get_ranked_lol_info(account["id"])

        if not ranked_queue:
                msg = "The summoner has not played any ranked games this season"

                updater.message.reply_text(msg)

        for league in ranked_queue:
            msg = ""
            msg +="Queue Type: {}\n".format(league["queue_type"])
            msg +="     Tier: {}\n".format(league["tier"])
            msg +="     Rank: {}\n".format(league["rank"])
            msg +="     Total Matches: {}\n".format(league["total_matches"])
            msg +="     Wins: {}\n".format(league["wins"])
            msg +="     Loses: {}\n".format(league["loses"])
            msg +="     Win Rate: {}\n".format(league["win_rate"])
            msg +="     PDL: {}\n".format(league["pdl"])

            updater.message.reply_text(msg)
    except KeyError:
        updater.message.reply_text("ERROR: Invalid Summoner")


def ranked_tft_info(updater, context):
    try:
        account = riot_api.update_account_secure_info("".join(context.args))
        league = riot_api.get_ranked_tft_info(account["id"])

        if not league:
                msg = "The summoner has not played any ranked tft games this season"
                
                updater.message.reply_text(msg)
        else:
            league = league[0]
            msg = ""
            msg +="Queue Type: {}\n".format(league["queue_type"])
            msg +="     Tier: {}\n".format(league["tier"])
            msg +="     Rank: {}\n".format(league["rank"])
            msg +="     Total Matches: {}\n".format(league["total_matches"])
            msg +="     1st places: {}\n".format(league["wins"])
            msg +="     Loses: {}\n".format(league["loses"])
            msg +="     Win Rate: {}\n".format(league["win_rate"])
            msg +="     PDL: {}\n".format(league["pdl"])

            updater.message.reply_text(msg)
    except KeyError:
        updater.message.reply_text("ERROR: Invalid Summoner")
     
    except Exception:
        updater.message.reply_text("Feature not yet available")
    

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Error "%s"', context.error)


def main():

    updater = Updater(con.bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_msg))
    dispatcher.add_handler(CommandHandler("help", help_msg))
    dispatcher.add_handler(CommandHandler("summoner", update_user, pass_args=True))
    dispatcher.add_handler(CommandHandler("mastery", mastered_champions, pass_args=True))
    dispatcher.add_handler(CommandHandler("lol", ranked_lol_info, pass_args=True))
    dispatcher.add_handler(CommandHandler("tft", ranked_tft_info, pass_args=True))
    
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
