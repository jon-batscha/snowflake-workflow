# Snowflake Workflow

This repo contains a few pre-built components to easily extract data from snowflake, optionally reshape it, and output the data to csv (either locally or to AWS). This package can be combined with the following packages:

- https://github.com/jon-batscha/config-csv-ingestion
- https://github.com/jon-batscha/s3_triggered_ingestion

to quickly set up a system to move your data from snowflake into Klaviyo, either for a one-off migration or as a recurring cron-job.

## Component Files

### `snowflake_to_csv.py`

This file contains the script that reads the config, along with your custom SQL file, to extract data from your snowflake warehouse

### `config.py`

This holds your credentials for snowflake, along with settings related to your warehouse, reshaping query, etc

### Not Included: your custom sql command file

As everyone's data is different: you will need to include a SQL query command file that snowflake can run to output the right data into a csv

## Run Instructions

1. Make sure `config.py` is properly configured
2. Make sure your custom sql file (e.g: `commands.sql`) is in the same directory as the other package components
3. Run `python snowflake_to_csv` (optionally, can include `--aws` to upload directly to configured s3 bucket)

## Dependencies

Written in `Python 3.8.3`, with packages in `requirements.txt`