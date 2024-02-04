from datetime import datetime
from airflow.decorators import dag, task
# from airflow.operators.papermill_operator import PapermillOperator
from airflow.utils.task_group import TaskGroup

from docker.types import Mount
from airflow.operators.empty import EmptyOperator

from src.config_settings import CeleryWorkers



default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2023, 4, 9),
        'retries': 0,
        'queue': CeleryWorkers.WORKER_2
    }

@dag(
    tags=["jupyter", "test", "papermill"],
    default_args=default_args,
    schedule_interval=None,
    catchup=False
    )
def jupyter_docker_dag():
    """Docker in Jupyter Notebook Test"""

    # src Packages
    from src.docker_settings import (
        DOCKER_API_VERSION,
        DockerCPU,
        DockerMemory,
        DockerNetwork,
        DockerUrl,
        DockerServiceMounts,
    )

    @task.docker(
        image="jupyter/base-notebook:latest",
        container_name="jupyter-test",
        #python_command="python 3.6",
        api_version=DOCKER_API_VERSION,
        docker_url=DockerUrl.PROXY,
        network_mode=DockerNetwork.HOST,
        mounts=DockerServiceMounts.COMMON_STAGE,
        # do_xcom_push=True,
        mount_tmp_dir=False,
        cpus=DockerCPU.FOUR,
        mem_limit=DockerMemory.EIGHT,
        auto_remove=True,
        user=0,
        working_dir="/opt/airflow/dags/notebooks",
    )
    def docker_task():
        import os
        os.system("pip install jupyter notebook papermill selenium")
        
        import papermill as pm
        import nbformat
        # from selenium import webdriver
        
        a = pm.execute_notebook(
        '/opt/airflow/dags/notebooks/my.ipynb',
        '/opt/airflow/dags/notebooks/output.ipynb',
        parameters = dict(param1=2),
        )
        
        # read the output notebook and access the outputs of cells
        with open('/opt/airflow/dags/notebooks/output.ipynb', 'r') as f:
            nb = nbformat.read(f, nbformat.NO_CONVERT)
            for cell in nb.cells:
                if cell.cell_type == 'code' and cell.outputs:
                    outputs = cell.outputs
                    print(outputs)
                    # do something with outputs
                    
        # read the output notebook and take screenshots of the output cells
        """
        with open('/opt/airflow/dags/notebooks/output.ipynb', 'r') as f:
            nb = nbformat.read(f, nbformat.NO_CONVERT)
            for i, cell in enumerate(nb.cells):
                if cell.cell_type == 'code' and cell.outputs:
                    # take screenshot of output cell
                    driver = webdriver.Chrome()
                    driver.set_window_size(1920, 1080)
                    driver.get('file:////opt/airflow/dags/notebooks/output.ipynb#{}'.format(i))
                    driver.save_screenshot('/opt/airflow/dags/ss_{}.png'.format(i))
                    driver.quit()
                return a
        """
        
        
    docker_jupyter = docker_task()
    
    docker_jupyter

jupyter_docker_dag = jupyter_docker_dag()
