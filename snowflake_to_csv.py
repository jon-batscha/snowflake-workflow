import snowflake.connector
import argparse
import config
import csv
import boto3

from sqlalchemy import create_engine

from sqlalchemy.dialects import registry
registry.register('snowflake', 'snowflake.sqlalchemy', 'dialect')

# get optional AWS arg
parser = argparse.ArgumentParser(description='automated workflow for extracting data from snowflake to s3 using standalone sql command file along with a config')
parser.add_argument('--aws', action='store_const', const = True, default= False, help='flag to upload data to s3')

args = parser.parse_args()
args_dict = vars(args)

# connect to snowflake
print("Connecting to Snowflake...")
engine = create_engine(
    'snowflake://{user}:{password}@{account}/'.format(
        user = config.snowflake_username,
        password = config.snowflake_password,
        account = config.account,
        database = config.database,
        schema = config.schema,
        warehouse = config.warehouse,
        role =config.role 
    )
)

# Execute basic setup command
connection = engine.connect()
connection.execute("USE DATABASE {database};".format(database = config.database))
connection.execute("USE WAREHOUSE {warehouse};".format(warehouse = config.warehouse))
connection.execute("ALTER WAREHOUSE {warehouse} SET WAREHOUSE_SIZE = '{warehouse_size}';".format(warehouse = config.warehouse, warehouse_size = config.warehouse_size)) 

# read sql commands from file, and get results from snowflake
with open(config.sql_query_file,'r') as f:
    query = f.read()

result = connection.execute(query)

output = [result._metadata.keys]

for row in result:

    output.append(list(row))

# write query results to output file
with open(config.output_filepath,'w') as f:
    writer = csv.writer(f)
    writer.writerows(output)

# optionally, upload to s3 bucket/folder
if args_dict['aws']:

    bucket_name = config.s3_bucket_location.split('/')[0]

    # set destination
    subfolders = [dir for dir in config.s3_bucket_location.split('/') if dir != '']

    if len(subfolders) == 1:

        dest = config.output_filepath

    else:

        dest = ''

        for dir in subfolders[1:]:

            dest += dir+'/'

        dest += config.output_filepath

    # send to destination
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    bucket.upload_file(config.output_filepath, dest)

connection.close()
engine.dispose()
