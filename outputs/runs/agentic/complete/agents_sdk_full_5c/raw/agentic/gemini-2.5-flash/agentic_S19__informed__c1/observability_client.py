
import os
from google.cloud import monitoring_v3

def get_monitoring_client():
    """
    Provides a configured Google Cloud Monitoring MetricServiceClient.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication.
    """
    return monitoring_v3.MetricServiceClient()

def get_gcp_project_id():
    """
    Retrieves the GCP project ID from environment variables or a default.
    """
    return os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
