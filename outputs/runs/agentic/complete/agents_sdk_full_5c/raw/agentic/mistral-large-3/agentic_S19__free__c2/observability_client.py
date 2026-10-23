import os
from google.cloud import monitoring_v3


def get_monitoring_client() -> monitoring_v3.MetricServiceClient:
    """Initialize and return a Google Cloud Monitoring client."""
    return monitoring_v3.MetricServiceClient()


def get_project_id() -> str:
    """Retrieve the Google Cloud project ID from environment variables."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")
    return project_id