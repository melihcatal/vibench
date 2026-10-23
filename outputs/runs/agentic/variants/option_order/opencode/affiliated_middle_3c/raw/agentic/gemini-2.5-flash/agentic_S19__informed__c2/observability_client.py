import os
from google.cloud import monitoring_v3


def get_metric_service_client():
    """Returns a Google Cloud Monitoring MetricServiceClient."""
    return monitoring_v3.MetricServiceClient()


def get_project_id():
    """Returns the Google Cloud project ID from environment variable or default."""
    return os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
