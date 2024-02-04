from typing import Tuple
from pathlib import Path
import time
from datetime import datetime


def _load_pythonpath(*args: Tuple[str]) -> str:
    """Load PYTHONPATH for Docker Microservices.

    Returns:
        str: List of PYTHONPATHs.
        
    Example:
        >>> _load_pythonpath("src", "src/test")
        "src:src/test"
    """
    return ':'.join(args)


def _load_services_from_dotenv(dotenv_path: Path) -> None:
    """Load Docker Microservice envs from .env file.

    Args:
        dotenv_path (Path): Path to .env file.
    """
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=dotenv_path)


def _load_container(svc: str):
    if not isinstance(svc, str):
        raise TypeError(f"Docker container name as a service must be str, got {type(svc)}")
    timestamp = str(int(time.time()))
    date_string = datetime.fromtimestamp(int(timestamp)).strftime('%d.%m.%y-%H.%M')
    return f"{svc}-{timestamp}"
    # return f"{svc}-{date_string}".replace("/", "_").replace(":", ".")
