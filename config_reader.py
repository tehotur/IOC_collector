import configparser


# Reads configuration values from the 'config.ini' file
def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config
