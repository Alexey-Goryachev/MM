import os
from bot import Bot
from logger import log_to_file
from time import sleep
from dotenv import load_dotenv


# Получаем данные для аутентификации из переменных окружения
load_dotenv()
# api_key = os.getenv('API_KEY')
# api_secret = os.getenv('API_SECRET')
# login = os.environ.get('LOGIN')
# password = os.environ.get('PASSWORD')
base_currency = os.environ.get('BASE_CURRENCY')  # Ваша базовая валюта
trading_pair = os.environ.get('TRADING_PAIR') # Ваша торговая пара

# Создаем экземпляр бота
bot = Bot(base_currency, trading_pair)

# Главный цикл работы бота
while True:
    try:
        bot.analyze_market()
        # if bot is None:
        #     break
    except Exception as e:
        log_to_file(f'Error: {str(e)}')
        
    # Возможно добавить  задержку, чтобы не перегружать биржу запросами
    sleep(60)
    #print(1) 
