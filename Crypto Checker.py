import telebot as bot
import requests

# DEFAULTS
TOKEN = 'PUT YOUR TOKEN HERE'
bot = bot.TeleBot(TOKEN)
URL = "https://api.binance.com/api/v3/ticker/price"


# BOT COMMANDS
@bot.message_handler(commands=['start', 'help'])
def greetings(message):
    bot.reply_to(message, "Here is the list for my commands: \n\n/price [ASSET] - Shows an asset's price\n\n/fee [ETH/BTC] - Shows the network's estimated fee (under maintenance)\n\n/currencies - Lists all the available currencies in DB")


@bot.message_handler(commands=['price'])
def show_price(message):  # /PRICE COMMAND
    symbol = message.text.upper()
    symbol = symbol[7:]
    botrequest = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT')
    if botrequest.status_code == 200:
        data = botrequest.json()
        data["price"] = "{:,.2f}".format(float(data["price"]))
        bot.reply_to(message, f'\n\n💰 {symbol}:  ${data["price"]}')

    elif botrequest.status_code == 400:
        bot.reply_to(message, "Asset not found! (Please use the abbreviations)")

    else:
        return


@bot.message_handler(commands=['currencies'])  # /CURRENCIES COMMAND
def currencies(message):
    botrequest = requests.get("https://api.binance.com/api/v3/ticker/price")
    data = botrequest.json()
    currencylist = []
    currencystring = ""
    for i in data[0:]:
        if i["symbol"].endswith("USDT"):
            currencylist.append(i["symbol"][:-4])
    for x in currencylist:
        currencystring += f"{x}, "
    bot.reply_to(message, currencystring[0:4096])


bot.infinity_polling()
