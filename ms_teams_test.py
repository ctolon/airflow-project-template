# Sys Packages
from datetime import datetime, timedelta
import pendulum

# Airflow Packages
from airflow.decorators import dag, task, task_group
from airflow.operators.empty import EmptyOperator
from airflow.utils.edgemodifier import Label
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from src.custom_dag_operators.ms_teams_webhook_operator import MSTeamsWebhookOperator

# Src Packages
from src.config_settings import CeleryWorkers

HOST = "127.0.0.1"
"""Airflow Webserver Hostname or IP Address."""


def on_failure(context):
    dag_id = context['dag_run'].dag_id

    task_id = context['task_instance'].task_id
    context['task_instance'].xcom_push(key=dag_id, value=True)

    logs_url = "https://{}/admin/airflow/log?dag_id={}&task_id={}&execution_date={}".format(
        HOST, dag_id, task_id, context['ts'])

    teams_notification = MSTeamsWebhookOperator(
        task_id="msteams_notify_failure",
        trigger_rule="all_done",
        message="`{}` has failed on task: `{}`".format(dag_id, task_id),
        button_text="View log", button_url=logs_url,
        theme_color="FF0000", http_conn_id='msteams_webhook_url')
    teams_notification.execute(context)


default_args = {
    'owner': 'cbtolon',
    'start_date': pendulum.datetime(2021, 1, 1, tz="Europe/Istanbul"),
    'retries': 0,
    'on_failure_callback': on_failure,
    'queue': CeleryWorkers.WORKER_1
}


@dag(
    "MS_Teams_test",
    description="MS Teams Operator Test",
    schedule=None,
    catchup=False,
    tags=["test", "ms-teams"],
    default_args=default_args,
)
def ms_teams_test():
    """MS-Teams Operator Test"""

    start, end = [EmptyOperator(task_id=tid, trigger_rule="all_done") for tid in ["start", "end"]]

    op1 = MSTeamsWebhookOperator(task_id='msteamtest',
        http_conn_id='msteams_webhook_url',
        message = "MS Teams Operator Test",
        subtitle = "This is the **subtitle**",
        theme_color = "00FF00",
        button_text = "My button",
        button_url = "https://www.google.com",
        #proxy = "https://yourproxy.domain:3128/",
        #dag=dag
        )

    start >> op1 >> end


ms_teams_test()
