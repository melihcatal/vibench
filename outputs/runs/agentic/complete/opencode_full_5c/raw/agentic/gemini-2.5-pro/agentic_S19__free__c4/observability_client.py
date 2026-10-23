import os
from google.cloud import monitoring_v3


def get_monitoring_client():
    """
    Initializes and returns a Google Cloud Monitoring client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    client = monitoring_v3.MetricServiceClient()
    return client, f"projects/{project_id}"


def get_project_id():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")
    return project_id
