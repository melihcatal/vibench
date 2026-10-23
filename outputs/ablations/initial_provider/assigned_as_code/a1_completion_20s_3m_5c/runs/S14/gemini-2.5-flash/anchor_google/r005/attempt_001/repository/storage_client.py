import os
from google.cloud import storage

def get_storage_client():
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")
    return storage.Client(project=project_id)
