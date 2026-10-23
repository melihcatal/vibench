import os
from google.cloud import monitoring_v3


def get_monitoring_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
    return monitoring_v3.MetricServiceClient()
