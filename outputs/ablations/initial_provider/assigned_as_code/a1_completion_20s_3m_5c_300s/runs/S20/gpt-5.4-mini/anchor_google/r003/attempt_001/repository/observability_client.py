import os

from google.cloud import logging_v2


def load_observability_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT"),
        "log_name": config.get("log_name") or os.environ.get("GOOGLE_CLOUD_LOG_NAME", "application"),
        "location": config.get("location") or os.environ.get("GOOGLE_CLOUD_LOCATION", "global"),
    }


def get_logging_client(config=None):
    cfg = load_observability_config(config)
    return logging_v2.Client(project=cfg["project_id"]), cfg
