"""Dummy End2End DAG for DE Projectt."""

# Sys Packages
from datetime import datetime, timedelta
import pendulum

# Airflow Packages
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule

from schemas.de_end2end_schema import EXAMPLE_SCHEMA

# src packages
from src.config_settings import CeleryWorkers

default_args = {
    'owner': 'cbtolon',
    'start_date': pendulum.datetime(2021, 1, 1, tz="Europe/Istanbul"),
    'retries': 0,
    'queue': CeleryWorkers.WORKER_1
}

all_params = {
    **EXAMPLE_SCHEMA.runtime_handle_schema,
    **EXAMPLE_SCHEMA.run_tasks_schema,
    **EXAMPLE_SCHEMA.example_schema,
    **EXAMPLE_SCHEMA.mlflow_schema
}


@dag(
    "DE_End2End_0_0_1",
    description="DE Taskflow project",
    schedule=None,
    catchup=False,
    tags=["DE", "ETL", "Task", "dataops" "micro-service", "python"],
    default_args=default_args,
    params=all_params
    # schedule_interval=timedelta(hours=3),
    # on_success_callback=remove_containers(container_list=["...""]),
)
def etl_pipeline():
    """Automated DAG Workflow"""

    # src Packages
    from src.utils.cfg_loaders import _load_container
    from src.docker_settings import (
        PROJECT_DIR,
        DOCKER_DATA_DIR,
        DOCKER_API_VERSION,
        DockerCPU,
        DockerGPU,
        DockerMemory,
        DockerNetwork,
        DockerUrl,
        CommonDockerService,
        DockerServiceMounts,
        DockerDataProcessDirs
    )

    start, end = [EmptyOperator(task_id=tid, trigger_rule="all_done") for tid in ["start", "end"]]
    # data_num_success =  EmptyOperator(task_id="data_number_success")
    # data_validation_success = EmptyOperator(task_id="data_validation_success")
    
    data_validation_success = EmptyOperator(task_id="data_validation_success")

    @task(provide_context=True, default_args=default_args)
    def init_temp_datastore(**context) -> bool:
        """
        #### This function creates a temporary datastore for docker tasks.
        """

        from pathlib import Path
        dir = DockerDataProcessDirs.EXAMPLE
        if context["params"]["workflow-tasks"]["init-datastore"] is False:
            print("init-temp-datastore is set to False. Skipping...")
            return True

        print(f"Datastore creating for docker tasks at {dir} ...")
        Path.mkdir(dir, exist_ok=False, parents=True)
        print(f"Datastore created successfully!: {dir}")
        return True

    @task(provide_context=True, default_args=default_args, multiple_outputs=True)
    def run_initial_params(**context) -> dict:
        """
        #### This function sets initial parameters for the pipeline as JSONs.
        """
        from pprint import pprint
        import time

        all_params = context["params"]
        print("All params: ")
        pprint(all_params)
        epoch = {"initial-epoch": {"value": int(time.time())}}
        all_params = {**all_params, **epoch}
        return all_params

    @task.docker(
        image=CommonDockerService.MLFLOW_IMG,
        container_name=_load_container(CommonDockerService.MLFLOW_SVC),
        api_version=DOCKER_API_VERSION,
        docker_url=DockerUrl.PROXY,
        network_mode=DockerNetwork.HOST,
        mounts=DockerServiceMounts.COMMON_STAGE,
        mount_tmp_dir=False,
        cpus=DockerCPU.FOUR,
        device_requests=DockerGPU.NONE,
        mem_limit=DockerMemory.EIGHT,
        auto_remove=True,
        multiple_outputs=True,
        user=0,
        working_dir=DockerDataProcessDirs.EXAMPLEw.as_posix(),
        #environment={
        #    'PYTHONPATH': ...
        #    'LIBS_TO_INJECT': ...
        #}
    )
    def run_check_number_of_datas(initial_params_response: dict) -> dict:
        """
        #### It checks whether there is enough document for machine learning training according to a specified threshold value.
        If there is enough document, Pipeline continues to next step. Otherwise, it stops.
        """

        # Dependency Injection 
        import sys
        import os
        sys.path = sys.path + os.environ["LIBS_TO_INJECT"].split(':')

        from src.config_settings import INIConfigs
        from src.autoconfig import extract_args_from_dict_as_namespace
        from projects import example_code
        from pprint import pprint

        print(f"Variables From Check Docname List: {initial_params_response} ")

        if initial_params_response["workflow-tasks"]["example"] == False:
            print("run-check-docname-list is set to False. Skipping...")
            return initial_params_response

        args = extract_args_from_dict_as_namespace(initial_params_response, "example")

        # Set Variables been pushed from previous task

        # Set Configs
        args.example_logger_config = f"{INIConfigs.LOGGER}"

        print("Airflow Config:")
        pprint(args)

        # Call Function and Set Return Values
        return_dict = example_code(args)
        initial_params_response["example"]["status"] = return_dict["status"]

        response = initial_params_response
        return response

    @task.branch(multiple_outputs=False, provide_context=True)
    def is_num_of_data_enough_for_etl(check_number_of_datas: dict, if_true: str, if_false: str, **kwargs):
        x = kwargs["ti"].xcom_pull(task_ids=check_number_of_datas)
        print(f"Variables From {check_number_of_datas}: ", x)
        if x.get("status") == "success":
            # kwargs["ti"].xcom_push(check_number_of_datas)
            return if_true
        else:
            return if_false

    @task.branch(multiple_outputs=False, provide_context=True)
    def is_num_of_data_enough_for_etl(check_number_of_datas: dict, if_true: str, if_false: str, **kwargs):
        from pprint import pprint
        x = kwargs["ti"].xcom_pull(task_ids=check_number_of_datas)

        print(f"Variables From {check_number_of_datas}: ")
        pprint(x)

        if x["workflow-tasks"]["run-check-docname-list"] is False:
            print("run-check-docname-list is set to False. Skipping...")
            return if_true

        if x["run-check-docname-list"]["status"] == "success":
            print("Data is enough for training!")
            print("Pipeline continues to next step...")
            # kwargs["ti"].xcom_push(check_number_of_datas)
            return if_true
        else:
            return if_false

    @task(multiple_outputs=True, provide_context=True)
    def data_number_success(**kwargs):
        response = kwargs["ti"].xcom_pull(task_ids="run_check_number_of_datas")
        if response["workflow-tasks"]["run-check-docname-list"] is False:
            print("run-check-docname-list is set to False. Skipping...")
            return response
        return response

    @task.docker(
        image=CommonDockerService.MLFLOW_IMG,
        container_name=_load_container(CommonDockerService.MLFLOW_SVC),
        api_version=DOCKER_API_VERSION,
        docker_url=DockerUrl.PROXY,
        network_mode=DockerNetwork.HOST,
        mounts=DockerServiceMounts.COMMON_STAGE,
        mount_tmp_dir=False,
        cpus=DockerCPU.FOUR,
        device_requests=DockerGPU.NONE,
        mem_limit=DockerMemory.EIGHT,
        auto_remove=True,
        user=0,
        multiple_outputs=True,
        working_dir=DockerDataProcessDirs.EXAMPLE.as_posix(),
        #environment={
        #    'PYTHONPATH': ...
        #    'LIBS_TO_INJECT': ...
        #}
    )
    def run_fetch_data_from_s3(data_num_success_response: dict, **kwargs) -> dict:
        """
        #### This function runs fetch_data_from_s3 process for Fetching Data From DB and then it Labels Datas.
        """

        ...

    @task()
    def data_number_failed():
        return False

    @task.docker(
        image=CommonDockerService.MLFLOW_IMG,
        container_name=_load_container(CommonDockerService.MLFLOW_SVC),
        api_version=DOCKER_API_VERSION,
        docker_url=DockerUrl.PROXY,
        network_mode=DockerNetwork.HOST,
        mounts=DockerServiceMounts.COMMON_STAGE,
        mount_tmp_dir=False,
        cpus=DockerCPU.FOUR,
        device_requests=DockerGPU.NONE,
        mem_limit=DockerMemory.EIGHT,
        auto_remove=True,
        user=0,
        multiple_outputs=True,
        working_dir=DockerDataProcessDirs.EXAMPLE.as_posix(),
        #environment={
        #    'PYTHONPATH': ...
        #    'LIBS_TO_INJECT': ...
        #}
    )
    def run_remove_emojis(fetch_data_from_s3_response: dict, **kwargs) -> dict:

        ...

    @task.docker(
        image=CommonDockerService.MLFLOW_IMG,
        container_name=_load_container(CommonDockerService.MLFLOW_SVC),
        api_version=DOCKER_API_VERSION,
        docker_url=DockerUrl.PROXY,
        network_mode=DockerNetwork.HOST,
        mounts=DockerServiceMounts.COMMON_STAGE,
        mount_tmp_dir=False,
        cpus=DockerCPU.FOUR,
        device_requests=DockerGPU.NONE,
        mem_limit=DockerMemory.EIGHT,
        auto_remove=True,
        user=0,
        multiple_outputs=True,
        working_dir=DockerDataProcessDirs.EXAMPLE.as_posix(),
        #environment={
        #    'PYTHONPATH': ...
        #    'LIBS_TO_INJECT': ...
        #}
    )
    def run_null_handler(remove_emojis_response: dict, **kwargs) -> dict:

        ...

    @task.docker(
        image=CommonDockerService.MLFLOW_IMG,
        container_name=_load_container(CommonDockerService.MLFLOW_SVC),
        api_version=DOCKER_API_VERSION,
        docker_url=DockerUrl.PROXY,
        network_mode=DockerNetwork.HOST,
        mounts=DockerServiceMounts.COMMON_STAGE,
        mount_tmp_dir=False,
        cpus=DockerCPU.FOUR,
        device_requests=DockerGPU.NONE,
        mem_limit=DockerMemory.EIGHT,
        auto_remove=True,
        user=0,
        multiple_outputs=True,
        working_dir=DockerDataProcessDirs.EXAMPLE.as_posix(),
        #environment={
        #    'PYTHONPATH': ...
        #    'LIBS_TO_INJECT': ...
        #}
    )
    def run_missing_handler(build_vocab_response: dict, **kwargs) -> dict:

        ...

    @task.docker(
        image=CommonDockerService.MLFLOW_IMG,
        container_name=_load_container(CommonDockerService.MLFLOW_SVC),
        api_version=DOCKER_API_VERSION,
        docker_url=DockerUrl.PROXY,
        network_mode=DockerNetwork.HOST,
        mounts=DockerServiceMounts.COMMON_STAGE,
        mount_tmp_dir=False,
        cpus=DockerCPU.FOUR,
        device_requests=DockerGPU.NONE,
        mem_limit=DockerMemory.EIGHT,
        auto_remove=True,
        user=0,
        working_dir=DockerDataProcessDirs.EXAMPLE.as_posix(),
        #environment={
        #    'PYTHONPATH': ...
        #    'LIBS_TO_INJECT': ...
        #}
    )
    def run_train(build_embeddings_response: dict, **kwargs) -> dict:

        ...

    @task.docker(
        image=CommonDockerService.MLFLOW_IMG,
        container_name=_load_container(CommonDockerService.MLFLOW_SVC),
        api_version=DOCKER_API_VERSION,
        docker_url=DockerUrl.PROXY,
        network_mode=DockerNetwork.HOST,
        mounts=DockerServiceMounts.COMMON_STAGE,
        mount_tmp_dir=False,
        cpus=DockerCPU.FOUR,
        device_requests=DockerGPU.NONE,
        mem_limit=DockerMemory.EIGHT,
        auto_remove=True,
        user=0,
        working_dir=DockerDataProcessDirs.EXAMPLE.as_posix(),
        #environment={
        #    'PYTHONPATH': ...
        #    'LIBS_TO_INJECT': ...
        #}
    )
    def run_save_model_to_mlflow(train_response: dict, **context) -> str:

        ...

    @task()
    def data_validation_failed():
        return False

    @task()
    def data_validation():
        return True

    @task.branch()
    def is_data_valid_for_deploy(task_ids: str, if_true: str, if_false: str, **kwargs):
        x = kwargs["ti"].xcom_pull(task_ids=task_ids)
        if x is True:
            return if_true
        else:
            return if_false

    @task()
    def CI_CD():
        return True

    @task()
    def data_validation_failed():
        return False

    @task.docker(
        image=CommonDockerService.MLFLOW_IMG,
        container_name=_load_container(CommonDockerService.MLFLOW_SVC),
        api_version=DOCKER_API_VERSION,
        docker_url=DockerUrl.PROXY,
        network_mode=DockerNetwork.HOST,
        mounts=DockerServiceMounts.DELETE_STAGE,
        mount_tmp_dir=False,
        cpus=DockerCPU.FOUR,
        device_requests=DockerGPU.NONE,
        mem_limit=DockerMemory.EIGHT,
        auto_remove=True,
        user=0,
        working_dir=DOCKER_DATA_DIR,
        environment={'PYTHONPATH': PROJECT_DIR},
        trigger_rule=TriggerRule.ALL_DONE
    )
    def remove_datas():

        import sys
        import os
        import shutil
        sys.path.append("/opt/airflow/dags")
        from src.docker_settings import DockerDataProcessDirs

        dir = DockerDataProcessDirs.EXAMPLE

        # Check DAGs are currently running or not (DAGs has 3 states as success, failed and running)
        if os.path.exists(dir):
            print(f"Temp Datastore Found in {dir} it will be removed ...")
            try:
                shutil.rmtree(dir)
                print(f"{dir} removed successfully.")
            except Exception as e:
                print(f"{dir}: {e}")
        return True

    # DAG Dependencies
    create_datastore = init_temp_datastore()
    fetch_params = run_initial_params()
    check_number_of_data = run_check_number_of_datas(fetch_params)
    decision_for_data_num = is_num_of_data_enough_for_etl("run_check_number_of_datas", "data_number_success",
                                                        "data_number_failed")
    data_num_success = data_number_success()
    data_number_error = data_number_failed()
    fetch_data_from_s3 = run_fetch_data_from_s3(data_num_success)
    remove_emojis = run_remove_emojis(fetch_data_from_s3)
    handle_null_vals = run_null_handler(remove_emojis)
    handle_missing = run_missing_handler(handle_null_vals)
    run_ml_train = run_train(handle_missing)
    save_model = run_save_model_to_mlflow(run_ml_train)
    data_validation_result = data_validation()
    data_validation_decision = is_data_valid_for_deploy("data_validation", "data_validation_success",
                                                          "data_validation_failed")
    model_deployment_result = CI_CD()
    data_validation_error = data_validation_failed()
    # remove_data_files = remove_datas()

    # Set Dag Dependencies Example
    start >> create_datastore >> fetch_params >> check_number_of_data >> decision_for_data_num
#
    decision_for_data_num >> data_num_success >> fetch_data_from_s3 >> remove_emojis >> handle_null_vals >> handle_missing >> run_ml_train >> save_model >> data_validation_result >> data_validation_decision
    decision_for_data_num >> data_number_error >> end
#
    data_validation_decision >> data_validation_success >> model_deployment_result >> end
    data_validation_decision >> data_validation_error >> end


etl_pipeline()
