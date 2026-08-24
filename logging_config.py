import logging
from logging.handlers import RotatingFileHandler

def setup_logging_debug(level=logging.DEBUG):
    handler = RotatingFileHandler(
        "logs.log",
        maxBytes=1024*10, #в килобайтах
        backupCount=0,
        encoding="utf-8"
    )
    handler.flush = True
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    handler.setFormatter(formatter)
    handler.setLevel(level)

    logging.basicConfig(
        level=level,
        handlers=[handler]
    )