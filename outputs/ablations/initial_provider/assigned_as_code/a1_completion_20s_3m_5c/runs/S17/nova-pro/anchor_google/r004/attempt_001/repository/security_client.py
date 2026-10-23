import os
from google.cloud import kms

def get_client():
    return kms.KeyManagementServiceClient()

def get_config():
    return {
        "project_id": os.getenv("PROJECT_ID"),
        "location": os.getenv("LOCATION"),
        "key_ring": os.getenv("KEY_RING"),
        "key_id": os.getenv("KEY_ID")
    }