import os
from google.cloud import monitoring_v3


def get_monitoring_client():
    """
    Initializes and returns a Google Cloud Monitoring client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return monitoring_v3.MetricServiceClient()


def get_project_id():
    """
    Retrieves the Google Cloud project ID from environment variables.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id
