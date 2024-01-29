import os
from dotenv import load_dotenv
import requests 

from logger import logger

load_dotenv()


class Exchange:
    def __init__(self, base_currency, trading_pair, currency_price):
        # Initialization of variables for interaction with the exchange API
        self.base_currency = base_currency
        self.trading_pair = trading_pair
        self.currency_price = currency_price
        self.login = os.environ.get('LOGIN')
        self.password = os.environ.get('PASSWORD')
        self.base_url = 'http://185.197.251.129/public/v1' 

        # Call the authenticate method when creating an Exchange object
        self.authenticate()

    def authenticate(self):
        # Authentication logic on the exchange
        authentication_data = {
            'username': os.environ.get('LOGIN'),
            'password': os.environ.get('PASSWORD'),
        }

        headers = {'Content-Type': 'application/json'}

        try:
            response_auth = requests.post(f'{self.base_url}/login/', json=authentication_data, headers=headers)

            # Check whether authentication was successful
            response_auth.raise_for_status()
            authentication = response_auth.json()
            self.token_auth = authentication['token']
            
            token_verify = {'token': self.token_auth}
            
            try:
                response_token_verify = requests.post(f'{self.base_url}/token/verify/', json=token_verify, headers=headers)

                response_token_verify.raise_for_status()
                logger.info(f'Token is valid {response_token_verify.text}')
            except Exception as e:
                # Print an error message with a response code, if available
                status_code = getattr(e, 'response', None)
                logger.info(status_code)
                if status_code is not None:
                    logger.error(f'Authentication failed token verify: {str(e)}, Status code: {status_code}')
                else:
                    logger.error(f'Authentication failed token verify: {str(e)}')
                    return f'Authentication failed token verify'
        except Exception as e:
            # Print an error message with a response code, if available
            status_code = getattr(e, 'response', None)
            logger.info(status_code)
            if status_code is not None:
                logger.error(f'Authentication failed: {str(e)}, Status code: {status_code}')
            else:
                logger.error(f'Authentication failed: {str(e)}')
                return f'Authentication failed'

    
            

    def get_current_prices(self, side):
        # Getting current prices of an asset
        params = {
            'pair': f'{self.trading_pair}',
            'side': side  
        }

        try:
            response = requests.get(f'{self.base_url}/exchange/order-book/', params=params)
            response.raise_for_status()

            #Getting data on trades
            self.prices_response = response.json()
           
            #Get a list of current prices
            prices = []
            for price in self.prices_response[side]:
                prices.append(price['unit_price'])
            
            return prices  
        except requests.exceptions.RequestException as e:
            logger.error(f'Error getting current prices: {str(e)}')
            return f'Error getting current prices: {str(e)}'
        
    def place_order(self, amount, unit_price, currency_pair, type):
        # Placing an order on the exchange
        data = {'amount': f'{amount}', 'unit_price': f'{unit_price}', 'currency_pair': f'{currency_pair}', 'type': f'{type}'}

        headers = {'Content-Type': 'application/json', 'Authorization': f'JWT {self.token_auth}'}

        try:
            response = requests.post(f'{self.base_url}/exchange/user/orders/', json=data, headers=headers)

            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logger.error(f'Error place_order {type}: {str(e)}')
            return f'Error place_order {type}: {str(e)}'

    def get_my_balance(self, current):
        # Getting personal balance
            
        params = {"currency": {"abbreviation": current}}

        headers = {'Content-Type': 'application/json', 'Authorization': f'JWT {self.token_auth}'}

        try:
            response = requests.get(f'{self.base_url}/user/balances/', json=params, headers=headers)

            response.raise_for_status()

            balance_response = response.json()
            

            currency_count = ""
            for currency in balance_response:
                if currency['currency']['abbreviation'] == current:
                    currency_count = currency['active_balance']
                    return currency_count
                else:
                    continue
        except requests.exceptions.RequestException as e:
            logger.error(f'Error get my balance: {str(e)}')
            return f'Error get my balance: {str(e)}'