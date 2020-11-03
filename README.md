**Shopify daily pipeline**
==========================

Introduction
------------
This application will extract daily data from AWS S3 and load the result into a PostgreSQL instance. The [source code](https://github.com/xiaoxiao-24/shopigy-daily/blob/main/shopify_daily_postgres.py) is written in python. It will get the extraction date from an env viariable DATE_CONFIG and execute.

Things need to be configured before:

*  Credentials are in a config file: [Credential.ini](https://github.com/xiaoxiao-24/shopigy-daily/blob/main/Credential.example.ini) .
>> \- Set AWS S3 credentials and bucket 

>> \- Set PostgreSQL credentials and db,table info 

* The extraction date can be set via the env variable DATE_CONFIG.


Build docker image
------------------
Edit [Dockerfile](https://github.com/xiaoxiao-24/shopigy-daily/blob/main/Dockerfile) and build image:
> $ docker build -t shopify_daily .
>

Run with docker
---------------
Change the extraction date to the one you what and run:
> $ docker run --rm -e DATE_CONFIG="2019-04-02" shopify_daily
>

Run with docker-compose
-----------------------
Edit [docker_compose.yml](https://github.com/xiaoxiao-24/shopigy-daily/blob/main/docker-compose.yml) to put your extraction date and run
> $ docker-compose up
>

Run with airflow
----------------
Deploy this [\*.dag](https://github.com/xiaoxiao-24/shopigy-daily/blob/main/test_dag_shopify.py) file to your airflow dag path and activate it via airflow web 
