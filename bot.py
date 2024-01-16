import os
from exchange import Exchange
import random
from dotenv import load_dotenv

from logger import logger

load_dotenv()

#Initializing the Bot class
class Bot(Exchange):

    def __init__(self, base_currency, trading_pair, currency_price):
        super().__init__(base_currency, trading_pair, currency_price)
        
    
    def analyze_market(self):
        # Market analysis and bidding decisions
        self.sellings = self.get_current_prices(side='selling')
        self.buyings = self.get_current_prices(side='buying')
        self.activity = ""
        for self.sell in self.sellings:
            if self.sell < self.currency_price:
                self.activity = f"Buy {self.base_currency}"
                return
            else:
                break #TODO double check, there's really no need to check other prices
        for self.buy in self.buyings:
            if self.buy > self.currency_price:
                self.activity = f"Sell {self.base_currency}"
                return
            else:
                break #TODO double check, there's really no need to check other prices
        

        
    def buy_asset(self):
        # Buying an asset on the exchange
        currency = os.environ.get('QUOTE')
        my_balance = self.get_my_balance(currency)
        logger.info(f"My balance in {currency} = {my_balance}")
        limit_for_end_bot = os.environ.get('QUOTE_MIN_BALANCE')
        if float(my_balance) > float(limit_for_end_bot):
            self.get_current_prices(side='selling')
            order = self.prices_response['selling'][0]
            logger.info(order) 
            self.place_order(order['volume'], order['unit_price'], order['pair'], type='buying')
        else:
            logger.warning(f'My balance {currency} lower, then minimum. Top up your balance ')
            return  "break"
        
        
    def sell_asset(self):
       # Selling an asset on the exchange
        currency = os.environ.get('BASE')
        my_balance = self.get_my_balance(currency)
        #balance_for_trade = round(float(my_balance) * 0.5, int(os.environ.get('BASE_PRECISION')))
        logger.info(f"My balance in {self.base_currency} = {my_balance}")
        #logger.info(f"My balance for trade in {self.base_currency} = {balance_for_trade}")
        limit_for_end_bot = os.environ.get('BASE_MIN_BALANCE')
        if float(my_balance) > float(limit_for_end_bot):
            self.buyings = self.get_current_prices(side='buying')
            order = self.prices_response['buying'][0]
            logger.info(order)
            self.place_order(order['volume'], order['unit_price'], order['pair'], type='selling')
            # if round(float(order['volume']) / 2 , int(os.environ.get('BASE_PRECISION'))) <= float(my_balance) <= round(float(order['volume']), int(os.environ.get('BASE_PRECISION'))):
            #     self.place_order(round(random.uniform(0, balance_for_trade), int(os.environ.get('BASE_PRECISION'))), order['unit_price'], order['pair'], type='selling')
            # else:
            #     self.buy_sell_youself(float(self.currency_price), self.trading_pair)
            
          
        else:
            logger.warning(f'My balance {currency} lower, then minimum. Top up your balance ')
            return  "break"

    
        
    def buy_sell_youself(self, unit_price, currency_pair):
        # Buying/selling an asset itself
        limit = os.environ.get('LIMIT_TRADE')
        type = random.choice(['selling', 'buying'])
        limit_price = os.environ.get('DEVIATION')
        
        amount = round(random.uniform(0, float(limit)), int(os.environ.get('BASE_PRECISION')))
        
        if type == 'selling':
            # If the type is selling, set the price slightly higher than the current one
            price_variation = round(random.uniform(0, float(limit_price)), int(os.environ.get('BASE_PRECISION')))
            unt_price = round(unit_price - price_variation, int(os.environ.get('BASE_PRECISION')))
            self.place_order(amount=amount, unit_price=unt_price, currency_pair=currency_pair, type=type)
            logger.info(f"Order {type} yourself create")

        elif type == 'buying':
            # If the type is buying, set the price slightly lower than the current one
            price_variation = round(random.uniform(0, float(limit_price)), int(os.environ.get('BASE_PRECISION')))
            unt_price = round(unit_price + price_variation, int(os.environ.get('BASE_PRECISION')))

            self.place_order(amount=amount, unit_price=unt_price, currency_pair=currency_pair, type=type)
            logger.info(f"Order {type} yourself create")
