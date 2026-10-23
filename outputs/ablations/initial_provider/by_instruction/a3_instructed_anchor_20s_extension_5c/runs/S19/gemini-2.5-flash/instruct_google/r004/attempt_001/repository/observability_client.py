from google.cloud import monitoring_v3
import os

def get_monitoring_client():
    """Returns a Google Cloud Monitoring MetricServiceClient."""
    return monitoring_v3.MetricServiceClient()

def get_project_id():
    """Returns the Google Cloud Project ID from environment variables or default."""
    # In a real application, consider using google.auth.default() to get project ID
    # or explicitly passing it.
    return os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
