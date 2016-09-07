#tousdbot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler, Filters
import logging
import requests
import json


"""
Takes a user's message eg: 165 MYR, and returns: 40.56 USD
All else returns error / "try again"

Should be able to use in a group chat as follows: @tousdbot 135 SGD


BOT TOKEN: insert_token_here

"""



updater = Updater(token='insert_token_here')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#each function corresponds to a command that a bot can take

def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Submit eg: '100 EUR' and I'll convert it to USD")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)



def convert(bot, update, args):
	try:
		amount = int(args[0])
		print amount
		currency = args[1]
		print currency
		#Make USD-USD Conversion exception case
		if currency == "USD":
			usdcase = str(amount) + " " + str(currency) + "  ->  " + str(amount) + " " + str(currency)
			bot.sendMessage(chat_id=update.message.chat_id, text = usdcase)
		else:
			#use google api here to get conversion and extract from json returned
			request_url = "http://rate-exchange.herokuapp.com/fetchRate?from=" + currency + "&to=USD"
			r = requests.get(request_url)
			req_json = r.json()
			x_rate = float(req_json['Rate'])


			new_amount = x_rate*amount

			conversion = str(amount) + " " + str(currency) + "  ->  " + str(new_amount) + " USD"

			bot.sendMessage(chat_id = update.message.chat_id, text = conversion)
	except:
		error_msg = "Submission format incorrect, eg: '100 EUR'"
		bot.sendMessage(chat_id=update.message.chat_id, text = error_msg)



convert_handler = CommandHandler('convert', convert, pass_args=True)
dispatcher.add_handler(convert_handler)
"""




"""
def inline_convert(bot, update):
	#query format should be e.g: 184 MYR
	query = update.inline_query.query
	if not query:
		return
	results = list()
	args_inline = query.split(" ")

	#Copying from convert function
	try:
		amount = int(args_inline[0])
		currency = args_inline[1]
		#Make USD-USD Conversion exception case
		if currency == "USD":
			usdcase = str(amount) + " " + str(currency) + "  ->  " + str(amount) + " " + str(currency)
			conversion_inline = usdcase
		else:
			#use google api here to get conversion and extract from json returned
			request_url = "http://rate-exchange.herokuapp.com/fetchRate?from=" + currency + "&to=USD"
			r = requests.get(request_url)
			req_json = r.json()
			x_rate = float(req_json['Rate'])

			new_amount = x_rate*amount

			conversion_inline = str(amount) + " " + str(currency) + "  ->  " + str(new_amount) + " USD"

	except:
		error_msg = "Submission format incorrect, eg: '100 EUR'"
		conversion_inline = error_msg

	results.append(
		InlineQueryResultArticle(
			id=query,
			title = conversion_inline,
			input_message_content=InputTextMessageContent(conversion_inline)

			)

		)
	bot.answerInlineQuery(update.inline_query.id, results)

inline_convert_handler = InlineQueryHandler(inline_convert)
dispatcher.add_handler(inline_convert_handler)


def help(bot, update):
	help_msg = "The tousdbot Help Guide: \n\n /start : Shows bot description.\n/convert : Converts given currency amount into USD, eg: '100 EUR'.\n\n The bot can be used inline by doing, eg: '@tousdbot 100 EUR', and waiting for the menu to show the conversion which can then be selected and sent to the whole chat as a message."
	bot.sendMessage(chat_id=update.message.chat_id, text= help_msg)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)



def unknown(bot, update):
	 bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler([Filters.command], unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()




