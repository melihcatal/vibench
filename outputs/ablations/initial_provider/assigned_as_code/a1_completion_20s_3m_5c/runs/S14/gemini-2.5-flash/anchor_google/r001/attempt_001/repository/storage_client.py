from google.cloud import storage
import os

def get_storage_client(project_id: str):
    return storage.Client(project=project_id)

def get_bucket_name():
    return os.environ.get("GCS_BUCKET_NAME", "your-gcs-bucket-name")

def get_project_id():
    return os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
