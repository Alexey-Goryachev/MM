import os
from dotenv import load_dotenv
import requests 
#import json


load_dotenv()


class Exchange:
    def __init__(self, base_currency, trading_pair):
        # Инициализация переменных для взаимодействия с API биржи
        self.base_currency = base_currency
        self.trading_pair = trading_pair
        self.login = os.environ.get('LOGIN')
        self.password = os.environ.get('PASSWORD')
        self.base_url = 'https://richamster.com/public/v1' 

        # Вызываем метод authenticate при создании объекта Exchange
        self.authenticate()

    def authenticate(self):
        # Логика аутентификации на бирже
        # Используйте self.api_key и self.api_secret для передачи данных аутентификации в запросы API
        authentication_data = {
            'username': os.environ.get('LOGIN'),
            'password': os.environ.get('PASSWORD'),
        }

        headers = {'Content-Type': 'application/json'}

        try:
            print(f"Request URL: {self.base_url}/login")
            print(f"Request Data: {authentication_data}")
            response = requests.post(f'{self.base_url}/login', json=authentication_data, headers=headers)
            print(response.text)

        # Проверка успешности аутентификации
            response.raise_for_status()

        except Exception as e:
            # Выводим сообщение об ошибке с кодом ответа, если он доступен
            status_code = getattr(e, 'response', None)
            print(status_code)
            if status_code is not None:
                print(f'Authentication failed: {str(e)}, Status code: {status_code}')
            else:
                raise Exception(f'Authentication failed: {str(e)}')
            
    def get_current_prices(self):
        # Получение текущих цен актива
        params = {
            'pair': f'{self.trading_pair}',
            'side': 'buy'  # или 'sell' в зависимости от того, что вам нужно
        }

        try:
            response = requests.get(f'{self.base_url}/exchange/order-book/', params=params)
            response.raise_for_status()

            # Распечатываем полученные цены
            prices = response.json()
            print(prices)

        except requests.exceptions.RequestException as e:
            print(f'Error getting current prices: {str(e)}')
            raise

    def place_order(self, order_type, price, quantity):
        # Размещение ордера на бирже
        pass
