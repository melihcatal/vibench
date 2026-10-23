import os
from google.cloud import monitoring_v3

def get_monitoring_client():
    """Returns a Google Cloud Monitoring client."""
    return monitoring_v3.MetricServiceClient()

def get_project_id():
    """Retrieves the Google Cloud project ID from environment variables."""
    # This assumes GOOGLE_CLOUD_PROJECT environment variable is set.
    # Alternatively, the client library can often infer it.
    return os.getenv("GOOGLE_CLOUD_PROJECT")
