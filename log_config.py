import logging


# Getting the root logger and setting its level to DEBUG
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Logging message format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Logging to file settings
file_handler = logging.FileHandler('ioc.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Logging to console settings
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Connecting both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)