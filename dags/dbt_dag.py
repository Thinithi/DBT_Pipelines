"""
## dbt Snowflake TaskFlow DAG

This DAG uses Airflow's TaskFlow API to run a dbt project on Snowflake.
It runs `dbt run` using a virtual environment inside the Airflow container.

To work, ensure:
- Your dbt project exists at `/usr/local/airflow/dags/dbt/data_pipeline`
- The dbt virtualenv is installed at `$AIRFLOW_HOME/dbt_venv`
- Your `profiles.yml` is inside the correct directory (adjust --profiles-dir accordingly)

This DAG runs daily and prints the output of `dbt run`.
"""

from airflow.decorators import dag, task
from pendulum import datetime
import subprocess
import os

@dag(
    start_date=datetime(2023, 9, 10),
    schedule="@daily",
    catchup=False,
    default_args={"owner": "dbt", "retries": 1},
    tags=["dbt", "snowflake"],
    doc_md=__doc__,
)
def dbt_run_taskflow():
    @task
    def run_dbt():
        """
        Task to run dbt using the CLI.
        """
        dbt_path =  "dbt"
        project_path = "/usr/local/airflow/dags/dbt/data_pipelines"
        profiles_path = "/usr/local/airflow/dags/dbt/data_pipelines"

        try:
            result = subprocess.run(
                [dbt_path, "run", "--project-dir", project_path, "--profiles-dir", profiles_path],
                capture_output=True,
                text=True,
            )
            result.check_returncode()
            print("dbt run succeeded:\n", result.stdout)
            return "Success"
        except subprocess.CalledProcessError as e:
            print("dbt run failed:\n", e.stderr)
            raise

    @task
    def notify(result: str):
        """
        Print confirmation.
        """
        print(f"dbt task finished with result: {result}")

    notify(run_dbt())

# Instantiate the DAG
dbt_run_taskflow()



