from google.cloud import monitoring_v3
import os

def get_monitoring_client():
    """Initializes and returns a Google Cloud Monitoring client."""
    return monitoring_v3.MetricServiceClient()

def get_project_name():
    """Gets the project name from environment variables for API calls."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return f"projects/{project_id}"
