Shopify daily pipeline

Introduction

Run with docker
change the execution date to the one you need and run:
$ docker run --rm -e DATE_CONFIG="2019-04-02" shopify_daily

Run with docker-compose
edit docker_compose.yml to put your execution date and run
$ docker-compose up

Run with airflow
put the *.dag to your airflow dag path and activate it