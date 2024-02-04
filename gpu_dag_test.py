# Sys Packages
import pendulum

# Airflow Packages
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator

# Src Packages
from src.config_settings import CeleryWorkers

default_args = {
    'owner': 'cbtolon',
    'start_date': pendulum.datetime(2021, 1, 1, tz="Europe/Istanbul"),
    'retries': 0,
    'queue': CeleryWorkers.WORKER_2
}


@dag(
    "GPU_test",
    description="NVIDIA-CUDA GPU test",
    schedule=None,
    catchup=False,
    tags=["gpu", "test", "nvidia", "cuda", "python 3.8.15"],
    default_args=default_args,
)
def gpu_test_dag():
    """NVIDIA-GPU Test Dag. It will test the GPU and CUDA availability on the system."""

    # src Packages
    from src.docker_settings import (
        DOCKER_API_VERSION,
        DockerCPU,
        DockerGPU,
        DockerMemory,
        DockerNetwork,
        DockerUrl,
    )

    start, end = [EmptyOperator(task_id=tid, trigger_rule="all_done") for tid in ["start", "end"]]

    @task.docker(
        image="tensorflow:latest",
        container_name="dag-gpu-test",
        api_version=DOCKER_API_VERSION,
        docker_url=DockerUrl.PROXY,
        network_mode=DockerNetwork.HOST,
        mount_tmp_dir=False,
        cpus=DockerCPU.FOUR,
        device_requests=DockerGPU.ENABLE,
        mem_limit=DockerMemory.EIGHT,
        auto_remove=True,
        user=0,
        working_dir="/tmp",
    )
    def gpu_test_task() -> bool:
        """#### GPU Test Task for NVIDIA-CUDA/Machine Learning"""
        import os
        from transformers import AutoModelForSequenceClassification
        import torch
        print("GPU INFO")
        os.system("nvidia-smi")

        DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        model = AutoModelForSequenceClassification.from_pretrained(
            'dbmdz/bert-base-turkish-cased')

        model.to('cuda:0')

        if DEVICE.type == "cuda":
            print(torch.cuda.get_device_name(0))
            print('Memory Usage:')
            print('Allocated:', round(torch.cuda.memory_allocated(0) / 1024 ** 3, 1), 'GB')
            print('Cached:   ', round(torch.cuda.memory_reserved(0) / 1024 ** 3, 1), 'GB')
            return True
        elif DEVICE.type == "cpu":
            print("Running on CPU")
            print(torch.cuda.get_device_name(0))
            print('Memory Usage:')
            print('Allocated:', round(torch.cuda.memory_allocated(0) / 1024 ** 3, 1), 'GB')
            print('Cached:   ', round(torch.cuda.memory_reserved(0) / 1024 ** 3, 1), 'GB')
            return False

    gpu_task = gpu_test_task()

    start >> gpu_task >> end


gpu_test_dag()
