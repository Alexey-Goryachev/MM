import os
from dotenv import load_dotenv
import requests 
import json


load_dotenv()


class Exchange:
    def __init__(self, base_currency, trading_pair, currency_price):
        # Инициализация переменных для взаимодействия с API биржи
        self.base_currency = base_currency
        self.trading_pair = trading_pair
        self.currency_price = currency_price
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
            response_auth = requests.post(f'{self.base_url}/login/', json=authentication_data, headers=headers)

        # Проверка успешности аутентификации
            response_auth.raise_for_status()
            authentication = response_auth.json()
            print(authentication)
            self.token_auth = authentication['token']
            
            token_verify = {'token': self.token_auth}
            
            try:
                response_token_verify = requests.post(f'{self.base_url}/token/verify/', json=token_verify, headers=headers)

                response_token_verify.raise_for_status()
                print(f'Token is valid {response_token_verify.text}')
            except Exception as e:
                # Выводим сообщение об ошибке с кодом ответа, если он доступен
                status_code = getattr(e, 'response', None)
                print(status_code)
                if status_code is not None:
                    print(f'Authentication failed: {str(e)}, Status code: {status_code}')
                else:
                    raise Exception(f'Authentication failed: {str(e)}')
        except Exception as e:
            # Выводим сообщение об ошибке с кодом ответа, если он доступен
            status_code = getattr(e, 'response', None)
            print(status_code)
            if status_code is not None:
                print(f'Authentication failed: {str(e)}, Status code: {status_code}')
            else:
                raise Exception(f'Authentication failed: {str(e)}')

    
            

    def get_current_prices(self, side='selling'):
        # Получение текущих цен актива
        params = {
            'pair': f'{self.trading_pair}',
            'side': side  
        }

        try:
            response = requests.get(f'{self.base_url}/exchange/order-book/', params=params)
            response.raise_for_status()

            # Распечатываем полученные цены
            self.prices_response = response.json()
            #print(self.prices_response)

            #Получаем список текущих цен
            prices = []
            for price in self.prices_response[side]:
                prices.append(price['unit_price'])
            
            return prices  
        except requests.exceptions.RequestException as e:
            print(f'Error getting current prices: {str(e)}')
            raise
        
    def place_order(self, amount, unit_price, currency_pair, type):
        # Размещение ордера на бирже
        data = {'amount': f'{amount}', 'unit_price': f'{unit_price}', 'currency_pair': f'{currency_pair}', 'type': f'{type}'}

        headers = {'Content-Type': 'application/json', 'Authorization': f'JWT {self.token_auth}'}

        try:
            response = requests.post(f'{self.base_url}/exchange/user/orders/', json=data, headers=headers)

            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f'Error getting current prices: {str(e)}')
            raise
        
