import os

from google.cloud import monitoring_v3
from google.cloud import storage


def load_observability_config(config=None):
    config = dict(config or {})
    if "project_id" not in config:
        config["project_id"] = os.environ["GOOGLE_CLOUD_PROJECT"]
    return config


def monitoring_client():
    return monitoring_v3.MetricServiceClient()


def storage_client():
    return storage.Client()


def project_name(config):
    return f"projects/{load_observability_config(config)['project_id']}"
