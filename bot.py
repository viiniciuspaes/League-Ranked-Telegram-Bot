import telegram
import logging
import riot_api
import constants as con
from telegram.ext import Updater, CommandHandler, MessageHandler


def help_msg(bot, updater):
    msg = ""

def start_msg(bot, updater):
    msg = "What can this bot do?\n"\
        "League ranked info is a bot that allows you to check "\
        "some basic ranked info from: \n"\
        "\n- League of Legends"\
        "\n- Teamfight Tactics"\
        "\n- Legends of Runeterra(Comming soon)\n"\
        "\n- You will be able to verify: "\
        "\n- wins"\
        "\n- Looses"\
        "\n- Win rate"\
        "\n- Tier"\
        "\n- Rank"\
        "\n- PDL"\
        "\n- Total valid matches"\
        "\n- All of this with a simple chat message."\
        "\nThis bot was created by Vinicius \"Torack\" Paes,"\
        "as a open source project."\
        "\nCheck on:\n https://github.com/viiniciuspaes/League-Ranked-Telegram-Bot"

    updater.message.reply_text(msg)


def update_user(bot, updater, args):
    account_info = riot_api.update_account_secure_info(args)
    msg = "Summoner Name: {}\n"\
        "Summoner Level: {}\n"\
        "Last Update: {}\n"\
        "Acount id {}".format(account_info["name"],
                        account_info["summoner_level"],
                        account_info["revision"],
                        account_info["id"])
    updater.message.reply_text(msg)

def mastered_champions(bot, updater, args):
    account = riot_api.update_account_secure_info(args)
    number = riot_api.get_mastered_lol_champions(account["id"])
    updater.message.reply_text("Account {} has {} mastered champions"\
    .format(account["name"], number))

def ranked_lol_info(bot, updater,args):
    account = riot_api.update_account_secure_info(args)
    ranked_queue = riot_api.get_ranked_lol_info(account["id"])

    for league in ranked_queue:
        msg = ""
        msg += "Queue Type: {}\n".format(league["queue_type"])
        msg +="     Tier: {}\n".format(league["tier"])
        msg +="     Rank: {}\n".format(league["rank"])
        msg +="     Total Matches: {}\n".format(league["total_matches"])
        msg +="     Wins: {}\n".format(league["wins"])
        msg +="     Loses: {}\n".format(league["loses"])
        msg +="     Win Rate: {}\n".format(league["win_rate"])
        msg +="     PDL: {}\n".format(league["pdl"])

        updater.message.reply_text(msg)

def ranked_tft_info(bot, updater, args):
     account = riot_api.update_account_secure_info(args)
     ranked_queue = riot_api.get_ranked_tft_info(account["id"])
     for league in ranked_queue:
        msg = ""
        msg += "Queue Type: {}\n".format(league["queue_type"])
        msg +="     Tier: {}\n".format(league["tier"])
        msg +="     Rank: {}\n".format(league["rank"])
        msg +="     Total Matches: {}\n".format(league["total_matches"])
        msg +="     Wins: {}\n".format(league["wins"])
        msg +="     Loses: {}\n".format(league["loses"])
        msg +="     Win Rate: {}\n".format(league["win_rate"])
        msg +="     PDL: {}\n".format(league["pdl"])

        updater.message.reply_text(msg)

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    bot = telegram.Bot(token=con.bot_token) #remove this int he future
    updater = Updater(token=con.bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_msg))
    dispatcher.add_handler(CommandHandler("help", help_msg))
    dispatcher.add_handler(CommandHandler("summonerName", update_user, pass_args=True))
    dispatcher.add_handler(CommandHandler("masteredChampions", mastered_champions, pass_args=True))
    dispatcher.add_handler(CommandHandler("rankedLol", ranked_lol_info, pass_args=True))
    dispatcher.add_handler(CommandHandler("rankedTft", ranked_tft_info, pass_args=True))

    updater.idle()

if __name__ == "__main__":
    main()

# print(bot.get_me())
