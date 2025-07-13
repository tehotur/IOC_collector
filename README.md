# IOC Collector

This project parses Indicators of Compromise (IOCs) from two different sources, detects their type and stores the data into a PostgreSQL database.

## What does the script do

- Loads configuration from `config.ini` with file paths and database information.
- Parses CSV or text data from `URLhaus` and `AlienVault`.
- Detects the type of IOC (IP, domain, unknown).
- Creates a PostgreSQL table `iocs`.
- Inserts the parsed IOCs into the table with timestamp, ioc type and source.

##  Requirements
- Python 3.12+
- PostgreSQL running and accessible

## How to install
Create and activate virtual environment
```
python -m venv venv
# Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```
You can install all dependencies using:
```
pip install -r requirements.txt
```
Change your database information and add paths in the configuration file config.ini
```
[paths]
urlhaus = path/to/urlhaus
alienvault = path/to/alienvault

[database]
host = localhost
port = 5432
user = your_user
password = your_password
dbname = your_db

```
## How to run
Run the script with:
```
python ioc_collector.py
```
All logs will be stored in ioc.log and printed to the console.
