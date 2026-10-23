import os
from google.cloud import storage
from functools import lru_cache

@lru_cache(maxsize=1)
def get_storage_client() -> storage.Client:
    """
    Initializes and returns a Google Cloud Storage client.
    
    Assumes application default credentials are configured.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    # The client will automatically use the project from the environment
    # if the project_id argument is not provided.
    client = storage.Client(project=project_id)
    return client

def get_default_bucket_name() -> str:
    """
    Retrieves the default GCS bucket name from an environment variable.
    """
    return os.environ.get("GCS_BUCKET_NAME", "")
