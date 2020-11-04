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

# get execution date 
if os.getenv("DATE_CONFIG") is None or os.getenv("DATE_CONFIG") == '':
    date_arg = config['ExecutionDate']['DATE_CONFIG']
else:
    date_arg = os.getenv("DATE_CONFIG")

# s3 credentials
if os.getenv("AWS_ACCESS_KEY_ID") is None or os.getenv("AWS_ACCESS_KEY_ID") == '':
    AWS_Access_Key_ID = config['AWS S3']['AWS_ACCESS_KEY_ID']
else:
    AWS_Access_Key_ID = os.getenv("AWS_ACCESS_KEY_ID")
print(AWS_Access_Key_ID)

if os.getenv("AWS_SECRET_KEY") is None or os.getenv("AWS_SECRET_KEY") == '':
    AWS_Secret_Key = config['AWS S3']['AWS_SECRET_KEY']
else:
    AWS_Secret_Key = os.getenv("AWS_SECRET_KEY")
print(AWS_Secret_Key)

if os.getenv("BUCKET_NAME") is None or os.getenv("BUCKET_NAME") == '':
    BUCKET_NAME = config['AWS S3']['BUCKET_NAME']
else:
    BUCKET_NAME = os.getenv("BUCKET_NAME")
print(BUCKET_NAME)

#KEY = '2019-04-01.csv'
KEY = date_arg+'.csv'
print("Process data: ", KEY)

# db credentials
if os.getenv("DB_TYPE") is None or os.getenv("DB_TYPE") == '':
    db_type = config['PostgreSQL']['DB_TYPE']
else:
    db_type = os.getenv("DB_TYPE")

if os.getenv("DB_IP") is None or os.getenv("DB_IP") == '':
    db_ip = config['PostgreSQL']['DB_IP']
else:
    db_ip = os.getenv("DB_IP")

if os.getenv("DB_PORT") is None or os.getenv("DB_PORT") == '':
    db_port = config['PostgreSQL']['DB_PORT']
else:
    db_port = os.getenv("DB_PORT")

if os.getenv("DB_PORT") is None or os.getenv("DB_PORT") == '':
    db_name = config['PostgreSQL']['DB_NAME']
else:
    db_name = os.getenv("DB_NAME")

if os.getenv("DB_USER") is None or os.getenv("DB_USER") == '':
    db_user = config['PostgreSQL']['DB_USER']
else:
    db_user = os.getenv("DB_USER")

if os.getenv("DB_PWD") is None or os.getenv("DB_PWD") == '':
    db_pwd = config['PostgreSQL']['DB_PWD']
else:
    db_pwd = os.getenv("DB_PWD")

if os.getenv("DB_TBL") is None or os.getenv("DB_TBL") == '':
    db_table = config['PostgreSQL']['DB_TBL']
else:
    db_table = os.getenv("DB_TBL")

# --------------------------------------------
# extract data from S3
# --------------------------------------------
s3c = boto3.client(
        's3', 
        aws_access_key_id = AWS_Access_Key_ID,
        aws_secret_access_key = AWS_Secret_Key
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

engine = create_engine('{}://{}:{}@{}:{}/{}'.format(db_type, db_user, db_pwd, db_ip, db_port, db_name))

if (engine.execute("select * from {} where export_date = '{}' ".format(db_table, str(date_arg))).fetchall() == []):
    df.to_sql(db_table, engine, if_exists='append', index=False)
else:
    print("Data of date '{}' already exist.".format(str(date_arg)))

