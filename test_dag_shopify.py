from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'xiaoxiao',
    'depends_on_past': False,
    'start_date': datetime(2019, 4, 1),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'end_date': datetime(2019, 4, 8),
}

dag = DAG('xx_test_shopify', default_args=default_args, schedule_interval='0 2 * * *')

t1 = DockerOperator(
                task_id='docker_command',
                image='xiaoxiaorey/shopify_daily:v4',
                api_version='auto',
                auto_remove=True,
                environment={ 
                    'DATE_CONFIG': "{{ ds }}" 
                },
                network_mode="bridge",
                dag = dag
)

t1

if __name__ == '__main__':
    dag.cli()
