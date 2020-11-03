FROM python:3.9.0
WORKDIR /app
RUN python -m pip install boto3
RUN python -m pip install pandas
RUN python -m pip install sqlalchemy
RUN python -m pip install psycopg2
COPY shopify_daily_postgres.py /app
COPY Credential.ini /app
ENV DATE_CONFIG="2019-04-01"
ENTRYPOINT ["python", "shopify_daily_postgres.py"]
