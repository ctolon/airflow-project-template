"""Docker Configurations Module File."""

from pathlib import Path
import os
# from src.submodule_utils.project_settings import *
from src.utils.cfg_loaders import _load_pythonpath, _load_services_from_dotenv


PROJECT_DIR = Path(__file__).parent.parent.resolve()
"""Top Level Dags Directory Absolute Path."""

COMPONENTS_DIR = Path(__file__).parent.parent.resolve() / "components"
"""Top Level Docker Microservice components Absolute Path."""

MICROSERVICE = COMPONENTS_DIR / "micro-service"
"""Microservice Architectural Components Directory Absolute Path."""

DOCKER_API_VERSION = "1.41"
"""Docker Engine API Version."""

DOCKER_DATA_DIR = PROJECT_DIR / "workflows"
"""Top Level Directory for Docker Tasks."""

CONTAINER_PROJECT_DIR = Path("/opt/airflow/dags")
"""Top Level Airflow Dags Directory Absolute Path in Docker Operator Containers."""

CONTAINER_DOCKER_DATA_DIR = CONTAINER_PROJECT_DIR / "workflows"


############
DE_PROJECTS = PROJECT_DIR / "projects"
"""Top Level Directory of DE Projects."""


class ProjectDirs(object):
    """Projects Dirs."""

    MLFLOW = DE_PROJECTS / "mlflow"
###########


class MLFlowScriptDirs(object):
    """Project Data Script Directories Absolute Paths."""

    MLFLOW_SRC = ProjectDirs.MLFLOW / "src/devops"


class DockerDotEnvPaths(object):
    """Microservice .env files Absolute Paths."""

    COMMON = MICROSERVICE / "common/.env"
    


class DockerServiceMounts(object):
    """Docker Service Mounts."""
    
    from docker.types import Mount

    COMMON_STAGE = [
        Mount(
            source=CONTAINER_PROJECT_DIR.as_posix(),
            target=CONTAINER_PROJECT_DIR.as_posix(),
            type="bind"
        ),
        Mount(
            source=CONTAINER_DOCKER_DATA_DIR.as_posix(),
            target=CONTAINER_DOCKER_DATA_DIR.as_posix(),
            type="bind"
        ),
    ]

    DELETE_STAGE = [
        Mount(
            source=CONTAINER_PROJECT_DIR.as_posix(),
            target=CONTAINER_PROJECT_DIR.as_posix(),
            type="bind"
        ),
        Mount(
            source=CONTAINER_DOCKER_DATA_DIR.as_posix(),
            target=CONTAINER_DOCKER_DATA_DIR.as_posix(),
            type="bind"
        )
    ]


class CommonDockerService(object):
    """Common Docker Microservice Components."""

    _load_services_from_dotenv(DockerDotEnvPaths.COMMON)

    MLFLOW_SVC = os.getenv('MLFLOW_SVC')
    MLFLOW_TAG = os.getenv('MLFLOW_TAG')
    MLFLOW_IMG = f"{MLFLOW_SVC}:{MLFLOW_TAG}"
    MLFLOW_PP = _load_pythonpath(ProjectDirs.MLFLOW.as_posix())

class ExampleDockerService(object):
    """Example Docker Microservice Components."""

    _load_services_from_dotenv(DockerDotEnvPaths.COMMON)

    EXAMPLE_SVC = os.getenv('EXAMPLE_SVC')
    EXAMPLE_TAG = os.getenv('EXAMPLE_TAG')
    EXAMPLE_IMG = f"{EXAMPLE_SVC}:{EXAMPLE_TAG}"
    EXAMPLE_PP = _load_pythonpath(
        ProjectDirs.MLFLOW.as_posix(),
        PROJECT_DIR.as_posix()
    )

class DockerDataProcessDirs(object):
    """Main Data Folders For Mounting on Docker Operator Tasks."""

    EXAMPLE = DOCKER_DATA_DIR / "example-svc"

class DockerUrl(object):
    """Docker Operator URL Selections."""

    STANDARD = "unix://var/run/docker.sock"
    PROXY = "tcp://docker-proxy:2375"


class DockerNetwork(object):
    """Docker Operator Network Selections."""

    BRIDGE = "bridge"
    HOST = "host"


class DockerCPU(object):
    """Docker CPU Selections."""

    ALL = None
    ONE = 1 / 1024
    TWO = 2 / 1024
    THREE = 3 / 1024
    FOUR = 4 / 1024
    FIVE = 5 / 1024
    SIX = 6 / 1024
    SEVEN = 7 / 1024
    EIGHT = 8 / 1024
    NINE = 9 / 1024
    TEN = 10 / 1024
    ELEVEN = 11 / 1024
    TWELVE = 12 / 1024
    THIRTEEN = 13 / 1024
    FOURTEEN = 14 / 1024
    FIFTEEN = 15 / 1024
    SIXTEEN = 16 / 1024


class DockerGPU(object):
    """Docker GPU Selections."""
    from docker.types import DeviceRequest

    ENABLE = [DeviceRequest(count=-1, capabilities=[['gpu']])]
    NONE = None


class DockerMemory(object):
    """Docker RAM Selections in GB."""

    ALL = None
    ONE = "1g"
    TWO = "2g"
    THREE = "3g"
    FOUR = "4g"
    FIVE = "5g"
    SIX = "6g"
    SEVEN = "7g"
    EIGHT = "8g"
    NINE = "9g"
    TEN = "10g"
    ELEVEN = "11g"
    TWELVE = "12g"
    THIRTEEN = "13g"
    FOURTEEN = "14g"
    FIFTEEN = "15g"
    SIXTEEN = "16g"


if __name__ == "__main__":
    print(DOCKER_DATA_DIR.as_posix())
