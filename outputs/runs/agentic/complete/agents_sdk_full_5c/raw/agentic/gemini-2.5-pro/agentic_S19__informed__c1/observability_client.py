from google.cloud import monitoring_v3
import os

def get_monitoring_client():
    """
    Initializes and returns a Google Cloud Monitoring client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return monitoring_v3.MetricServiceClient()

def get_project_id():
    """
    Retrieves the Google Cloud project ID.
    This is a simplified example; in a real app, this might come from instance metadata
    or be explicitly configured. The client library often finds it automatically.
    """
    # A common way to get project_id is from an env var, especially in non-GCP environments
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        # Fallback for local development or when credentials file has project_id
        try:
            import json
            creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            if creds_path:
                with open(creds_path, 'r') as f:
                    creds = json.load(f)
                    project_id = creds.get('project_id')
        except (IOError, json.JSONDecodeError):
            pass # Ignore errors if file is not found or malformed
    
    if not project_id:
        raise ValueError("Google Cloud project ID not found. Please set GOOGLE_CLOUD_PROJECT or ensure credentials file is valid.")

    return project_id

