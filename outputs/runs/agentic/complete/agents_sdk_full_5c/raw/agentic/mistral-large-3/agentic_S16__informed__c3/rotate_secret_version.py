import os
from security_client import get_secret_manager_client

def rotate_secret_version(secret_name: str, payload: str) -> str:
    """
    Rotate a secret version in Google Cloud Secret Manager and return the new version ID.
    """
    client = get_secret_manager_client()
    parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/{secret_name}"
    
    # Add new secret version
    response = client.add_secret_version(
        request={
            "parent": parent,
            "payload": {"data": payload.encode("UTF-8")}
        }
    )
    return response.name.split("/")[-1]