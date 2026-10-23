import os

from google.cloud import logging_v2


def load_config(config=None):
    config = dict(config or {})
    config.setdefault("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT"))
    config.setdefault("log_name", os.environ.get("LOG_NAME", "application-log"))
    config.setdefault("max_results", int(os.environ.get("LOG_MAX_RESULTS", "50")))
    config.setdefault("start_time", os.environ.get("LOG_START_TIME"))
    config.setdefault("end_time", os.environ.get("LOG_END_TIME"))
    return config


def build_client(config=None):
    config = load_config(config)
    return logging_v2.Client(project=config["project_id"]), config
