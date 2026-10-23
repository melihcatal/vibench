import os

from google.cloud import logging_v2


def load_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT"),
        "log_name": config.get("log_name") or os.environ.get("GOOGLE_CLOUD_LOG_NAME", "application-log"),
        "service_name": config.get("service_name") or os.environ.get("SERVICE_NAME", "app"),
    }


def get_logging_client(config=None):
    config = load_config(config)
    return logging_v2.Client(project=config["project_id"]), config
