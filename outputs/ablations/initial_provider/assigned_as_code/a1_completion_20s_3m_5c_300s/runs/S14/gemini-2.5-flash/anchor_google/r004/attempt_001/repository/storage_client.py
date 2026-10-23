from google.cloud import storage
import os

def get_storage_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")
    return storage.Client(project=project_id)
