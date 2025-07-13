import pandas as pd
from log_config import logging
from urllib.parse import urlparse
import ipaddress
import validators


def parse_urlhaus_ioc(file_path):
    try:
        # Read urlhaus data
        logging.debug(f'Parsing urlhaus data from {file_path}')
        df = pd.read_csv(file_path, delimiter=',', comment='#')

        # Extract the URL column
        url_column = df.iloc[:, 2]
        # Extract domain/IP part
        striped_ioc = url_column.map(lambda url: urlparse(url).netloc)
        # Remove port numbers if present
        striped_ioc = striped_ioc.apply(lambda ioc: ioc.split(':')[0])

        # Create a new DataFrame with a clean ioc column
        new_df = pd.DataFrame({'ioc': striped_ioc})
        
        # Detect the type of each IOC (IP, domain, or unknown)
        new_df['ioc_type'] = new_df['ioc'].apply(detect_ioc_type)
        logging.debug('Detecting ioc type')

        new_df['source'] = 'urlhaus'
        logging.info(f'Parsed {len(new_df)} entries from urlhaus')
        return new_df
    
    except Exception as e:
        logging.error(f'Failed to parse urlhaus data from {file_path}: {e}')
        return pd.DataFrame() # Return empty DataFrame on failure


def parse_alienvault_ioc(file_path):
    try:
        # Read alienvault data
        logging.debug(f'Parsing alienvault data from {file_path}')
        df = pd.read_csv(file_path, header=None, delimiter='#')

        # Extract IP column
        striped_ioc = df.iloc[:, 0]
        # Create a new DataFrame with a clean ioc column
        new_df = pd.DataFrame({'ioc': striped_ioc})

        # Detect the type of each IOC (IP, domain, or unknown)
        new_df['ioc_type'] = new_df['ioc'].apply(detect_ioc_type)
        logging.debug('Detecting ioc type')
        new_df['source'] = 'alienvault'
        logging.info(f'Parsed {len(new_df)} entries from alienvault')
        return new_df
    
    except Exception as e:
        logging.error(f'Failed to parse alienvault data from {file_path}: {e}')
        return pd.DataFrame() # Return empty DataFrame on failure

def detect_ioc_type(ioc):
    try: 
        ipaddress.ip_address(ioc)
        return 'ip'
    except ValueError:
        if validators.domain(ioc):
            return 'domain'
    return 'unknown'