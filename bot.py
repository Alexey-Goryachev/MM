from exchange import Exchange

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
        order = self.prices_response['buying'][0]
        print(order) 
        self.place_order(order['volume'], order['unit_price'], order['side'])


        pass
    def sell_asset(self, quantity, target_price):
        # Продажа актива на бирже
        pass
