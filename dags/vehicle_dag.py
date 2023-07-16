from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd
from datetime import datetime
from datetime import timedelta

default_args = {
    'start_date': datetime(2023, 7, 15, 2, 30),
	'owner': 'Medeiros&Medeiros',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('vehicles_dag', default_args = default_args)

def load_data():
    df = pd.read_csv('/opt/airflow/dags/datas/vehicle_data.csv')
    return df.to_dict()

def perform_analysis(**context):
    df = pd.DataFrame(context['task_instance'].xcom_pull(task_ids='load_data'))  # Pulling data from XCom

    # Count the number of each type of fuel per year
    fuel_by_year = df.groupby(['Year', 'fuelType1']).size().reset_index(name='Count')

    # Group by year and fuel type, counting the amount of each fuel type
    fuel_by_year = df.groupby(['Year', 'fuelType1'])['fuelType1'].count().unstack().reset_index()

    # Sort by year
    fuel_by_year = fuel_by_year.sort_values(by='Year')

    # Replacing null with 0
    fuel_by_year = fuel_by_year.fillna(0)

    # Writing the dataframe to a CSV file
    fuel_by_year.to_csv("/opt/airflow/dags/datas/fuel_by_year.csv", index=False)

def group_by_fuelType(**context):
    df = pd.DataFrame(context['task_instance'].xcom_pull(task_ids='load_data'))  # Pulling data from XCom

    # Group by fuel type and count the number of unique models
    df_grouped_type = df.groupby('fuelType1')['Model'].nunique().reset_index(name='num_models')

    # Sort by number of models (descending order)
    df_sorted_type = df_grouped_type.sort_values(by='num_models', ascending=False)

    # Deleting the null row
    df_sorted_type = df_sorted_type[df_sorted_type['fuelType1'].notna()]

    # Writing the dataframe to a CSV file
    df_sorted_type.to_csv("/opt/airflow/dags/datas/grouped_by_fuelType.csv", index=False)

def group_by_manufacturer(**context):
    df = pd.DataFrame(context['task_instance'].xcom_pull(task_ids='load_data'))  # Pulling data from XCom
    
    # Group by brand and fuel type and count the number of unique models
    df_grouped_num_model = df.groupby(['Manufacturer', 'fuelType1'])['Model'].nunique().reset_index(name='num_models')

    # Sort by brand and number of models (descending order)
    df_sorted_num_model = df_grouped_num_model.sort_values(by=['Manufacturer', 'num_models'], ascending=[True, False])

    # Replace null
    df_sorted = df_sorted_num_model.fillna({'Manufacturer': 'Unknown', 'fuelType1': 'Unknown', 'num_models': 0 })

    # Writing the dataframe to a CSV file
    df_sorted.to_csv("/opt/airflow/dags/datas/grouped_by_manufacturer.csv", index=False)

# Define tasks
t1 = PythonOperator(task_id='load_data', python_callable=load_data, dag=dag)
t2 = PythonOperator(task_id='perform_analysis', python_callable=perform_analysis, dag=dag)
t3 = PythonOperator(task_id='group_by_fuelType', python_callable=group_by_fuelType, dag=dag)
t4 = PythonOperator(task_id='group_by_manufacturer', python_callable=group_by_manufacturer, dag=dag)
success = BashOperator(task_id='success_task', bash_command="echo 'Success: Data analysis complete!'", dag=dag)

# Define dependencies
t1 >> [t2, t3, t4] >> success