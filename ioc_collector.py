from log_config import logging
from psycopg2 import OperationalError
from config_reader import read_config
from data_parsers import parse_urlhaus_ioc, parse_alienvault_ioc
import database as db


def main():
    conn = None # Initialize database connection variable
    try:
        # Load configuration from a config file
        config = read_config()

        # Establish a connection to the PostgreSQL database
        conn = db.connect_to_db(config)
        logging.info('Successfully connected to database')

        # Parse IOC data from both sources
        urlhause_data = parse_urlhaus_ioc(config['paths']['urlhaus'])
        alienvault_data = parse_alienvault_ioc(config['paths']['alienvault'])
        
        with conn.cursor() as cursor: 
            # Create the IOC table if it does not already exist
            cursor.execute(db.create_ioc_table())
            logging.info('Created ioc table in database')

            # Insert urlhaus data if not empty
            if not urlhause_data.empty:
                cursor.executemany(db.insert_ioc_data(), urlhause_data.values.tolist())
                logging.info('Inserted urlhause data into iocs table')
            else:
                logging.warning('No urlhaus data to insert')

            # Insert alienvault data if not empty
            if not alienvault_data.empty:
                cursor.executemany(db.insert_ioc_data(), alienvault_data.values.tolist())
                logging.info('Inserted alienvault data into iocs table')
            else:
                logging.warning('No alienvault data to insert')

        # Commit all changes to the database
        conn.commit()
        
    except OperationalError as e:
        logging.error(f'Database connection failed: {e}')

    except Exception as e:
        logging.error(f'Unexpected error: {e}')

    finally:
        # Ensure the database connection is properly closed
        if conn:
            conn.close()
            logging.debug('Database connection closed')
            

if __name__ == "__main__":
    main()