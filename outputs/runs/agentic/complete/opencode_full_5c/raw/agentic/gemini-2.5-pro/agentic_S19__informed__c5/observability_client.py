import os
from google.cloud import monitoring_v3


def get_monitoring_client():
    """
    Initializes and returns a Google Cloud Monitoring client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS are set in the environment.
    """
    return monitoring_v3.MetricServiceClient()


def get_project_id():
    """
    Retrieves the GCP Project ID from an environment variable.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")
    return project_id
