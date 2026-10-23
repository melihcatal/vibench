# HELPER
import os
from google.cloud import monitoring_v3

def get_monitoring_client():
    """Return an authenticated Monitoring (Stackdriver) client using Application Default Credentials."""
    # Loads credentials from environment or service account file.
    client = monitoring_v3.MetricServiceClient()
    # Optional: use a project-specific client if needed.
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT') or 'PROJECT_ID'
    client.projects = f'projects/{project_id}'
    return client
