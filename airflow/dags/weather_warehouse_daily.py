from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.common.sql.operators.sql import SQLCheckOperator

with DAG(
    "weather_warehouse_daily",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["portfolio", "elt", "dbt"],
) as dag:
    extract = BashOperator(task_id="extract_api_to_s3", bash_command="python -m src.extract_weather --output /tmp/weather_raw && aws s3 sync /tmp/weather_raw s3://$RAW_BUCKET/weather/")
    transform = GlueJobOperator(task_id="glue_transform", job_name="weather-transform", script_args={"--SOURCE_PATH": "s3://{{ var.value.raw_bucket }}/weather/", "--TARGET_PATH": "s3://{{ var.value.raw_bucket }}/weather_curated/"})
    dbt_build = BashOperator(task_id="dbt_build", bash_command="cd dbt_warehouse && dbt build --target prod --profiles-dir profiles")
    quality_gate = SQLCheckOperator(task_id="quality_gate", conn_id="snowflake_default", sql="SELECT COUNT(*) > 0 FROM WEATHER_ANALYTICS.ANALYTICS.MART_DAILY_CITY_WEATHER WHERE WEATHER_DATE = CURRENT_DATE();")
    extract >> transform >> dbt_build >> quality_gate
