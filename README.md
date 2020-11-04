# **Shopify daily pipeline**

Introduction
==========================
This application is a data pipeline which extracts daily data from AWS S3 and load the result into a SQL instance.

How to use
==========================

Config Variables
------------------

Variables
*  Credentials :
>> \- AWS S3 credentials and bucket 

>> \- PostgreSQL credentials and db,table info 

* The extraction date via variable DATE_CONFIG.

Configuration in different ways

1. can be configured in a config file [Credential.ini](https://github.com/xiaoxiao-24/shopigy-daily/blob/main/Credential.example.ini)

2. can be set directly in [docker-compose.yml](https://github.com/xiaoxiao-24/shopigy-daily/blob/main/docker-compose.yml) 

3. can be set in [Dockerfile](https://github.com/xiaoxiao-24/shopigy-daily/blob/main/Dockerfile) and rebuild the image.

4. can be set directly as environment variables

Run as python script
--------------------
> python shopify_daily_postgres.py

Run with docker
------------------
Make a [Dockerfile](https://github.com/xiaoxiao-24/shopigy-daily/blob/main/Dockerfile)

Build image:
> $ docker build -t shopify_daily .
>

Run docker image:
> $ docker run --rm -e DATE_CONFIG="2019-04-02" shopify_daily
>

Edit [docker_compose.yml](https://github.com/xiaoxiao-24/shopigy-daily/blob/main/docker-compose.yml) and run
> $ docker-compose up
>

The docker image [shopify_daily pipeline](https://hub.docker.com/repository/docker/xiaoxiaorey/shopify_daily) is available on docker hub.

Schedule with airflow
----------------
Use DockerOperator(or BashOperator).
Example [dag](https://github.com/xiaoxiao-24/shopigy-daily/blob/main/test_dag_shopify.py) here is using DockerOperator.


