#!/usr/bin/env python
import os
from bot import Bot
from logger import logger
from time import sleep
import asyncio

from dotenv import load_dotenv

from telegram import send_telegram_message


# Get authentication data from environment variables
load_dotenv()

base_currency = os.environ.get('BASE')  
trading_pair =  os.environ.get('BASE') + '/' + os.environ.get('QUOTE')
currency_price = os.environ.get('PRICE')

# Create object bot
bot = Bot(base_currency, trading_pair, currency_price)



# Main cycle of the bot
def main(currency_price, trading_pair):
    while True:
        try:
            bot.analyze_market()
            if bot.activity.startswith('Buy'):
                logger.info('Start code logic for buying a user asset')
                status = bot.buy_asset()
            elif bot.activity.startswith('Sell'):
                logger.info('Start code logic for selling a user asset')
                status = bot.sell_asset()
            else:
                logger.info('Start code logic for creating an order to sell/buy an asset through your turnover')
                status = bot.buy_sell_youself(float(currency_price), trading_pair)

            if status == "break":
                message = f'Good bye, top up your balance and restart'
                asyncio.run(send_telegram_message(os.environ.get('API_TOKEN_BOT'), os.environ.get('CHAT_ID'), message))
                logger.info(message)
                break
        except Exception as e:
            logger.error(f'Error: {str(e)}')
                
        #Some pause for don't over load exchange requests 
        sleep(int(os.environ.get('TIME_REQUEST')))
     
if __name__ == "__main__":
    main(currency_price, trading_pair)
