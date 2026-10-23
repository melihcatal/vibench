from google.cloud import monitoring_v3
import os

def get_monitoring_client():
    """Returns a configured Google Cloud Monitoring client."""
    return monitoring_v3.MetricServiceClient()

def get_project_id():
    """Retrieves the Google Cloud Project ID from environment variables or gcloud config."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not project_id:
        try:
            from google.auth import default
            _, project_id = default()
        except Exception:
            pass
    if not project_id:
        raise ValueError("Google Cloud Project ID not found. Set GOOGLE_CLOUD_PROJECT environment variable.")
    return project_id
