# Sys Packages
from datetime import datetime, timedelta
import time

# DAG Instance
from airflow import DAG

# Operators
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


CD_MOUNT = "cd mnt"
CD_TARGET = "cd /mnt/ml/datastore/embeddings"
LS_CMD = "ls"


# Total Pipeline command
PIPELINE_CMD = f"bash -c '\
echo "'"===START LOGGING SESSION==="'" && \
{ls_cmd} && \
{cd_mnt} && \
{ls_cmd} && \
echo "'"===END LOGGING SESSION==="'" '".format(
    cd_mnt=CD_TARGET,
    ls_cmd=LS_CMD
)


# DAG Instance
with DAG(
    'example_dag',
    description="test example dag",
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["test", "bash"],
    # default_args=default_args
) as dag:

    t1 = DockerOperator(
        task_id='example_dag_test',
        image="python:3.8",
        container_name=f"simple_test_{int(time.time())}",
        api_version='1.37',
        command=PIPELINE_CMD,
        docker_url="tcp://docker-proxy:2375",
        network_mode="host",
        mounts=[
            Mount(
                source="/home/ctolon",
                source="/home/ctolon",
                type="bind"
            )
        ],
        # do_xcom_push=True,
        mount_tmp_dir=False,
        cpus=2/1024,
        mem_limit="2g",
        auto_remove=True,
        user=0
    )

    t1
