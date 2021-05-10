# importing the required libraries
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago
import pandas as pd
import numpy as np
import json
from cowin_search import CowinApi
from datetime import datetime
from airflow.utils.email import send_email
import logging

logging.basicConfig(level=logging.DEBUG)

# These args will get passed on to the python operator
default_args = {
    'owner': 'akm',
    'depends_on_past': False,
    'start_date': datetime(2021, 5, 9, 17, 0),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'catchup': False,
}

# define the DAG
dag = DAG(
    'cowin_search_dag',
    default_args=default_args,
    description='Get the vaccine slot',
    dagrun_timeout=timedelta(minutes=2),
    schedule_interval='*/2 * * * *',
)


def cowin_search_function(
        state_name: str,
        district_name:str,
        date: tuple,
        vaccine_name: str,
        age: int,
):
    api = CowinApi()
    #res = api.get_centres_by_state_age_time(state_name, vaccine_name, date_range, age)
    res = api.get_centres_by_district(state_name, district_name, date, vaccine_name, age)
    logging.info("Extracted this df", res)
    return res.to_json(orient='records')


# define the first task
vaccine_search = PythonOperator(
    task_id='get_vaccine_status',
    python_callable=cowin_search_function,
    op_kwargs={
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "date": "10-05-2021",
        "vaccine_name": "COVISHIELD",
        "age": 18
    },
    provide_context=True,
    dag=dag,
)


def email_callback(**kwargs):
    results_str = kwargs['ti'].xcom_pull(task_ids='get_vaccine_status')
    data = json.loads(results_str)
    results_df = pd.json_normalize(data)
    logging.info("Received the df from xcom", results_df)
    if results_df.__len__() > 0:
        content = f"<b><h1>Vaccine available </h1><hr> {results_df.to_html()}  </b>"
        send_email(
            to=[
                "sample_email.com"
            ],
            subject='Vaccine availability alert',
            html_content=content,
        )
    else:
        print("No centres found")


notify_task = PythonOperator(
    task_id='notify_via_email',
    python_callable=email_callback,
    provide_context=True,
    dag=dag,
)

vaccine_search >> notify_task
