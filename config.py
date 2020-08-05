# snowflake account
snowflake_username = ''
snowflake_password = ''
account = ''

#snowflake query
sql_query_file = '' # eg: 'commands.sql'
schema = ''
database = ''
warehouse = ''
warehouse_size = 'X-Small' # pick appropriate size, e.g: 'X-Small'
role = 'ANALYST' 

#output
output_filepath = 'output.csv'

#optional, to upload to AWS S3 bucket
s3_bucket_location = 'yourbucketname/data' #can include folder, eg: your-bucket/data
