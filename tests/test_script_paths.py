import pytest
from pathlib import Path
import sys

sys.path.append("..")

from src.config_settings import *
from src.docker_settings import *


@pytest.fixture(scope="session")
def dags_dir():
    return PROJECT_DIR

  
def test_mlflow_script_dirs():
    assert MLFlowScriptDirs.MLFLOW_SRC.exists()
    assert MLFlowScriptDirs.MLFLOW_SRC.is_dir()
    

if __name__ == "__main__":
    script = Path(__file__).name
    pytest.main([script, "--cov=reports", "--cov-report=html"])