"""Main Configurations Module File."""

from pathlib import Path

# =======================
# TOP LEVEL DIRECTORIES #
# =======================

PROJECT_DIR = Path(__file__).parent.parent.resolve()
"""Top Level Airflow Dags Directory Absolute Path"""

CONFIGS_DIR = PROJECT_DIR / "configs"
"""Top Level Directory of Config Files"""

SCHEMAS_DIR = PROJECT_DIR / "schemas"
"""Top Level Directory of Json Schema Files"""

MASTER_NODE_IP = "WRITE IP HERE."
"""Airflow Master-Node IP."""


class ConfigDirs(object):
    """Parrent Directories of Config Files in Airflow - Dags."""

    INI_CONFIGS = CONFIGS_DIR / "ini"


class INIConfigs(object):
    """Config INI file paths."""

    CONFIG = ConfigDirs.INI_CONFIGS / "config.ini"
    CREDS = ConfigDirs.INI_CONFIGS / "crediantals.ini"
    LOGGER = ConfigDirs.INI_CONFIGS / "logger.ini"


class DataStores(object):
    """Datastores Absolute Directory Paths."""

    STATIC = Path("/mnt/nfs/static/")

    
class CeleryWorkers(object):
    """Airflow Workers Hostnames for queue selections."""
    
    WORKER_1 = "worker-1"
    """It's optimal for Heavy CPU Operations. Specifications:
    
    - CPU: ...
    - RAM: 180G
    - GPU: None.
    """
    
    WORKER_2="worker-2"
    """It's optimal for Heavy GPU Operations. Specifications:
    
    - CPU: ...
    - RAM: ...
    - GPU: Nvidia RTX 4090
    """


if __name__ == "__main__":
    """Print All Absolute Paths in config_settings."""

    print("PROJECT_DIR: ", PROJECT_DIR)
    print("CONFIGS_DIR: ", CONFIGS_DIR)
    print("SCHEMAS_DIR: ", SCHEMAS_DIR)
    print("ConfigDirs.INI_CONFIGS: ", ConfigDirs.INI_CONFIGS)
    print("INIConfigs.CONFIG: ", INIConfigs.CONFIG)
    print("INIConfigs.CREDS: ", INIConfigs.CREDS)
    print("INIConfigs.LOGGER: ", INIConfigs.LOGGER)
    print("DataStores.STATIC: ", DataStores.STATIC)
