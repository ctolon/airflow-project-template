import requests
import pytest
import docker

@pytest.fixture(scope="module")
def mlflow_server_url():
    return "http://localhost:5000"

@pytest.fixture(scope="module")
def minio_server_url():
    return "http://localhost:9001" # Mapped from 9000


#@pytest.fixture(scope="module")
#def docker_proxy_url():
    #return "tcp://192.168.1.131:2375"

def test_mlflow_server_connection(mlflow_server_url):
    try:
        response = requests.get(mlflow_server_url)
        assert response.status_code == 200, "Failed to connect to MLflow server"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to MLflow server: {e}")
        
def test_minio_server_connection(minio_server_url):
    try:
        response = requests.get(minio_server_url)
        assert response.status_code == 200, "Failed to connect to Minio server"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Minio server: {e}")

"""
def test_docker_proxy_connection(docker_proxy_url):
    try:
        client = docker.DockerClient(base_url=docker_proxy_url)
        client.ping()
    except Exception as e:
        pytest.fail(f"Failed to connect to Docker proxy server: {e}")
"""
