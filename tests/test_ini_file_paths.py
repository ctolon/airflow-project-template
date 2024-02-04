import pytest
from pathlib import Path
import sys

sys.path.append("..")

from src.config_settings import *
from src.docker_settings import *


@pytest.fixture(scope="session")
def dags_dir():
    return PROJECT_DIR


def test_ini_configs_dir():
    assert ConfigDirs.INI_CONFIGS.exists()
    assert ConfigDirs.INI_CONFIGS.is_dir()
    
def test_config_ini_file():
    assert INIConfigs.CONFIG.exists()
    assert INIConfigs.CONFIG.is_file()
    
def test_crediantals_ini_file():
    assert INIConfigs.CREDS.exists()
    assert INIConfigs.CREDS.is_file()
    
def test_logger_ini_file():
    assert INIConfigs.LOGGER.exists()
    assert INIConfigs.LOGGER.is_file()
    
if __name__ == "__main__":
    script = Path(__file__).name
    pytest.main([script, "--cov=reports", "--cov-report=html"])