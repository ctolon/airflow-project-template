import pytest
from pathlib import Path
import sys

sys.path.append("..")

from src.config_settings import *
from src.docker_settings import *


@pytest.fixture(scope="session")
def dags_dir():
    return PROJECT_DIR


@pytest.fixture(scope="session")
def configs_dir():
    return PROJECT_DIR / "configs"


@pytest.fixture(scope="session")
def DE_PROJECTS_dir():
    return PROJECT_DIR / "projects"


if __name__ == "__main__":
    script = Path(__file__).name
    pytest.main([script, "--cov=reports", "--cov-report=html"])