from airflow import DAG 
from airflow.operators.python import PythonOperator 
from datetime import datetime 
from etl.excel_to_snowflake_etl import excel_to_snowflake_etl 
from etl.new_task import new_task_function  # Import the new task function
from etl.ETL_S3_SNOWFLAKES import execute_snowflake_sql  # Import the Snowflake SQL execution function
from etl.sf_to_postgresql import sf_to_function  # Import the Snowflake to PostgreSQL function

with DAG( 
    dag_id="excel_to_snowflake", 
    start_date=datetime(2023, 1, 1), 
    schedule_interval="@daily", 
    catchup=False 
) as dag: 
    etl_task = PythonOperator( 
        task_id="excel_to_snowflake_etl", 
        python_callable=excel_to_snowflake_etl, 
        op_kwargs={ 
            "excel_path": "/opt/airflow/excel/AdventureWorks_Sales.xlsx", 
            "target_table": "target_table_name" 
        } 
    )

    new_task = PythonOperator(
        task_id="new_task",
        python_callable=new_task_function
    )

    execute_sql_task = PythonOperator(
        task_id="execute_snowflake_sql",
        python_callable=execute_snowflake_sql
    )

    sf_to_pg_task = PythonOperator(
        task_id="sf_to_postgresql",
        python_callable=sf_to_function
    )

    # Set task dependencies
    etl_task >> new_task
    execute_sql_task >> sf_to_pg_task
