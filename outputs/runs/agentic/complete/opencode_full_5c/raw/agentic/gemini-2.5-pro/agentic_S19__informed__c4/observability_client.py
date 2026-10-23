import os
from google.cloud import monitoring_v3


def get_monitoring_client():
    """
    Initializes and returns a Google Cloud Monitoring client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    try:
        client = monitoring_v3.MetricServiceClient()
        return client
    except Exception as e:
        print(f"Failed to initialize Google Cloud Monitoring client: {e}")
        # In a real application, you might handle this more gracefully.
        # For this example, we'll return None and let the caller handle it.
        return None


def get_project_id():
    """
    Retrieves the Google Cloud project ID from the environment.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set.")
    return project_id
