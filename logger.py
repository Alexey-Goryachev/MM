import logging
from datetime import datetime


def setup_logger(log_file_path):
    # Создаем объект логгера
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Создаем форматтер
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Создаем файловый обработчик
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Создаем консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Пример использования
logger = setup_logger("bot_log.txt")

# Ваш основной код...

# Пример логирования
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
