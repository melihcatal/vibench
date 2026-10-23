import os
from google.cloud import monitoring_v3

def get_monitoring_client():
    """Returns a Google Cloud Monitoring client."""
    return monitoring_v3.MetricServiceClient()

def get_project_id():
    """Returns the Google Cloud project ID from environment variable."""
    return os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("GCP_PROJECT"))

if __name__ == '__main__':
    # Example usage (for testing purposes)
    project_id = get_project_id()
    if project_id:
        print(f"Google Cloud Project ID: {project_id}")
    else:
        print("GOOGLE_CLOUD_PROJECT or GCP_PROJECT environment variable not set.")
    client = get_monitoring_client()
    print(f"Google Cloud Monitoring Client initialized: {client}")
