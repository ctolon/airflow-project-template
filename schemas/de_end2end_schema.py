"""DE Project JSON Schema for End2End ML Pipeline DAG."""
from airflow.models.param import Param

from src.docker_settings import *
from src.config_settings import *


class EXAMPLE_SCHEMA:
    runtime_handle_schema = {
        "runtime": Param(
            {
                "handle": True,
            },
            description="Runtime Handle for Epoch/Date and File Paths",
            schema={
                "type": "object",
                "minItems": 1,
                "required": [
                    "handle",
                ],
                "additionalProperties": False,
                "properties": {
                    "handle": {"type": "boolean"},
                },
            }
        ),
    }

    run_tasks_schema = {
        "workflow-tasks": Param(
            {
                "init-datastore": True,
                "example": True,
                "mlflow": True
            },
            description="Which Tasks Should be run for workflow?",
            schema={
                "type": "object",
                "minItems": 1,
                "required": [
                    "init-datastore",
                    "example",
                    "mlflow"
                ],
                "additionalProperties": False,
                "properties": {
                    "init-datastore": {"type": "boolean"},
                    "example": {"type": "boolean"},
                    "mlflow": {"type": "boolean"}
                },
            }
        ),
    }

    example_schema = {
        "run-labelmaker": Param(
            {
                "input_path": "/mnt/nfs/data.csv",
                "handle_nul_vals": True,
                "output_path": "/mnt/nfs/output.csv",
                "example_logger_config": INIConfigs.LOGGER.as_posix(),
            },
            description="Run Example",
            schema={
                "type": "object",
                "minItems": 1,
                "required": [
                    "input_path",
                    "handle_nul_vals",
                    "output_path",
                    "example_logger_config"
                ],
                "additionalProperties": False,
                "properties": {
                    "input_path": {"type": ["null", "string"]},
                    "handle_nul_vals": {"type": ["null", "boolean"]},
                    "output_path": {"type": "string"},
                    "example_logger_config": {"type": "string"},
                },
            }
        ),
    }

    mlflow_schema = {
        "save-model-to-mlflow": Param(
            {
                "set_tracking_uri": "http://localhost:5000",
                "set_artifact_uri": "http://localhost:9000",
                "set_artifact_location": "s3://mlflow",
            },
            description="Run MLflow",
            schema={
                "type": "object",
                "minItems": 1,
                "required": [
                    "set_tracking_uri",
                    "set_artifact_uri",
                    "set_artifact_location",
                ],
                "additionalProperties": False,
                "properties": {
                    "set_tracking_uri": {"type": "string"},
                    "set_artifact_uri": {"type": "string"},
                    "set_artifact_location": {"type": ["null", "string"]},
                },
            }
        )
    }
