from exchange import Exchange
import random


#from main import currency_price, trading_pair
from dotenv import load_dotenv

load_dotenv()

class Bot(Exchange):
    def __init__(self, base_currency, trading_pair, currency_price):
        super().__init__(base_currency, trading_pair, currency_price)
        # Инициализация дополнительных переменных бота
        self.currency_price = currency_price

    def analyze_market(self):
        # Анализ рынка и принятие решений о торгах
        self.sellings = self.get_current_prices(side='selling')
        self.buyings = self.get_current_prices(side='buying')
        self.activity = ""
        for self.sell in self.sellings:
            if self.sell < self.currency_price:
                self.activity = f"Buy {self.base_currency}"
            else:
                break #TODO перепроверить действительно нет надобности проверять остальные цены
        for self.buy in self.buyings:
            if self.buy > self.currency_price:
                self.activity = f"Sell {self.base_currency}"
            else:
                break #TODO перепроверить действительно нет надобности проверять остальные цены
        

        
    def buy_asset(self):
        # Покупка актива на бирже
        self.get_current_prices(side='selling')
        order = self.prices_response['selling'][0]
        print(order) 
        self.place_order(order['volume'], order['unit_price'], order['pair'], type='buying')
        
    def sell_asset(self):
        # Продажа актива на бирже
        self.buyings = self.get_current_prices(side='buying')
        order = self.prices_response['buying'][0]
        print(order) 
        self.place_order(order['volume'], order['unit_price'], order['pair'], type='selling')
        
    def buy_sell_youself(self, unit_price, currency_pair):
        # Покупка/продажа актива самого-себя
        limit = 4
        type = random.choice(['selling', 'buying'])
        
        amount = round(random.uniform(0, limit), 2)
        
        if type == 'selling':
            # Если тип продажи, установите цену немного выше текущей
            price_variation = round(random.uniform(0, 0.01), 2)
            unt_price = round(unit_price - price_variation, 2)
            self.place_order(amount=amount, unit_price=unt_price, currency_pair=currency_pair, type=type)
            print(f"Ордер {type} yourself создан")

        elif type == 'buying':
            # Если тип покупки, установите цену немного ниже текущей
            price_variation = round(random.uniform(0, 0.01), 2)
            unt_price = round(unit_price + price_variation, 2)

            self.place_order(amount=amount, unit_price=unt_price, currency_pair=currency_pair, type=type)
            print(f"Ордер {type} yourself создан")
