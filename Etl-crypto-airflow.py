from datetime import datetime

import pandas as pd
import json
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.http_sensor import HttpSensor
from airflow.utils.dates import days_ago
from google.cloud import bigquery
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from pathlib import Path

pd.set_option('display.float_format', lambda x: '%.3f' % x)

import requests

default_args = {
    "owner": "gabriel",
    #"start_date": days_ago(1)
	"start_date": '2021-01-01'
}

API = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum&vs_currencies=usd%2Ceur%2Cbrl&include_market_cap=true&include_last_updated_at=true"

def transforma(dtframe):
    dataT = dtframe.T.reset_index()
    dataT = dataT.rename({'index': 'id'}, axis=1)
    dataT['id'] = dataT['id'].astype(str)
    dataT['register_date'] = datetime.today().strftime('%Y-%m-%d')
    return dataT

def chamadaAPI(API):
    r = requests.get(API)
    json_response = r.json()
    data = pd.DataFrame(json_response)
    data = transforma(data)
    return data, json_response

def obter_valor(id_da_criptomoeda="bitcoin", sigla_fiat="usd",**context):
    data, json_response = chamadaAPI(API)
    if id_da_criptomoeda in json_response:
        moeda = f"{sigla_fiat}"
        context['ti'].xcom_push(key=f"Cotações", value=json_response)
        print(data)
    else:
        raise ValueError(f"Falha ao consumir dados da API para criptomoeda ({id_da_criptomoeda}) e fiat ({moeda})")
    
def carrega_bigquery():
    data, json_response = chamadaAPI(API)
    # Define target table in BQ
    target_table = 'analytics_engineer_case.crypto'
    project_id = "data-case-study-322621" 
    credential = service_account.Credentials.from_service_account_file('PATH')
        
        # Location for BQ job, it needs to match with destination table location
    job_location = "US"

        # Save Pandas dataframe to BQ
    data.to_gbq(target_table, project_id=project_id, if_exists='append',
                location=job_location, progress_bar=True, credentials=credential)

with DAG('stone_criptos_DAG', schedule_interval='0 7 * * *', default_args=default_args, catchup=False) as dag:
    begin = DummyOperator(
        task_id='begin'
    )

    obter_valores = PythonOperator(
        task_id='obter_valores',
        python_callable=obter_valor,
        provide_context=True
    )
    
    carregar_valores = PythonOperator(
        task_id='carregar_valores',
        python_callable= carrega_bigquery,
        provide_context=True
    )
    
    end = DummyOperator(
        task_id='end'
    )

    begin >> obter_valores >> carregar_valores >> end