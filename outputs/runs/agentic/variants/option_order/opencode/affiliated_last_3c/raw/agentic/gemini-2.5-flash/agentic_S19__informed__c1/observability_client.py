import os
from google.cloud import monitoring_v3


def get_monitoring_client():
    return monitoring_v3.MetricServiceClient()


def get_project_id():
    return os.environ.get("GOOGLE_CLOUD_PROJECT")
