import pytest
from pathlib import Path
import sys

sys.path.append("..")

from src.config_settings import *
from src.docker_settings import *

    
def test_data_store_dirs():
    assert DataStores.STATIC.exists()
    assert DataStores.STATIC.is_dir()



if __name__ == "__main__":
    script = Path(__file__).name
    pytest.main([script, "--cov=reports", "--cov-report=html"])