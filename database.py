import psycopg2
from log_config import logging


# Establish a connection to the PostgreSQL database using parameters from config
def connect_to_db(config):
    logging.debug('Attempting to connect to the database')
    return psycopg2.connect(
        host = config['database']['host'],
        port = config['database']['port'],
        user = config['database']['user'],
        password = config['database']['password'],
        dbname = config['database']['dbname']
    )

# SQL query to create the 'iocs' table if it does not already exist
def create_ioc_table():
    return '''
            CREATE TABLE IF NOT EXISTS iocs(
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ioc VARCHAR(255) NOT NULL,
                ioc_type VARCHAR(255) CHECK (ioc_type IN ('ip', 'domain', 'unknown')),
                source VARCHAR(255)
            );'''

# SQL query template to insert a new IOC record into the table
def insert_ioc_data():
    return '''
                INSERT INTO iocs (
                    ioc, 
                    ioc_type, 
                    source)
                VALUES
                    (%s, %s, %s)
                ;'''
