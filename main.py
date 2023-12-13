import os
from bot import Bot
from logger import log_to_file
from time import sleep
from dotenv import load_dotenv


# Get authentication data from environment variables
load_dotenv()

base_currency = os.environ.get('BASE_CURRENCY')  # Ваша базовая валюта
trading_pair = os.environ.get('TRADING_PAIR') # Ваша торговая пара
currency_price = os.environ.get('CURRENCY_PRICE')

# Create object bot
bot = Bot(base_currency, trading_pair, currency_price)

# Main cycle of the bot
while True:
    try:
        bot.analyze_market()
        if bot.activity.startswith('Buy'):
            print('Start code logic for buying a user asset')
            bot.buy_asset()
        elif bot.activity.startswith('Sell'):
            print('Start code logic for selling a user asset')
            bot.sell_asset()
        else:
            print('Start code logic for creating an order to sell/buy an asset through your turnover')
            bot.buy_sell_youself(float(currency_price), trading_pair)
    except Exception as e:
        log_to_file(f'Error: {str(e)}')
        
    #Some pause for don't over load exchange requests 
    sleep(60)
     
