import pandas as pd
import numpy as np
import boto3
import io
import sys
import os
from sqlalchemy import create_engine
import configparser

config = configparser.ConfigParser()
config.read('Credential.ini')

# --------------------------------------------
# extract data from S3
# --------------------------------------------

# get execution date from env variable
date_arg = os.getenv("DATE_CONFIG")

# data to extract
BUCKET_NAME = config['AWS S3']['BUCKET_NAME']
#KEY = '2019-04-01.csv'
KEY = str(date_arg)+'.csv'
print("Process data: ", KEY)

s3c = boto3.client(
        's3', 
        aws_access_key_id = config['AWS S3']['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key = config['AWS S3']['AWS_SECRET_KEY']
)

try:
    obj = s3c.get_object(Bucket = BUCKET_NAME , Key = KEY)
except:
    print("Oops!", sys.exc_info()[0], "occurred.")
    print("Access Denied! Problem in source data !")
    sys.exit()

df = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8')

# --------------------------------------------
# transform data 
# --------------------------------------------

# remove rows with empty "application_id"
df = df[df.application_id.notnull()]

# create colume 'has_specific_prefix' based on colume 'index_prefix'
df['has_specific_prefix'] = np.where(df['index_prefix'] == 'shopify_', True, False)

# --------------------------------------------
# load to postgres
# --------------------------------------------

db_type = config['PostgreSQL']['DB_TYPE']
db_ip = config['PostgreSQL']['DB_IP']
db_port = config['PostgreSQL']['DB_PORT']
db_name = config['PostgreSQL']['DB_NAME']
db_user = config['PostgreSQL']['DB_USER']
db_pwd = config['PostgreSQL']['DB_PWD']
db_table = config['PostgreSQL']['DB_TBL']

engine = create_engine('{}://{}:{}@{}:{}/{}'.format(db_type, db_user, db_pwd, db_ip, db_port, db_name))
df.to_sql(db_table, engine, if_exists='append', index=False)

