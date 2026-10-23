import os
import google.auth
from google.cloud import monitoring_v3

def get_gcp_project_id():
    """Gets the GCP project ID from the environment or default credentials."""
    try:
        _, project_id = google.auth.default()
        if project_id:
            return project_id
    except google.auth.exceptions.DefaultCredentialsError:
        pass
    
    project_id_from_env = os.environ.get("GCP_PROJECT_ID")
    if not project_id_from_env:
        raise ValueError("GCP_PROJECT_ID environment variable not set and default credentials not found.")
    return project_id_from_env


def get_monitoring_client():
    """Creates and returns a Google Cloud Monitoring API client."""
    return monitoring_v3.MetricServiceClient()
