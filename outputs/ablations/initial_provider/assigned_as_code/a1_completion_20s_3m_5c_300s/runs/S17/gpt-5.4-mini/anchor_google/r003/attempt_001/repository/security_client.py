import os
from google.cloud import kms


def load_security_config(config=None):
    config = config or {}
    merged = {
        "project_id": config.get("project_id") or os.getenv("GOOGLE_CLOUD_PROJECT"),
        "location": config.get("location") or os.getenv("GOOGLE_CLOUD_LOCATION", "global"),
        "key_ring": config.get("key_ring") or os.getenv("GOOGLE_CLOUD_KEY_RING"),
        "key_id": config.get("key_id") or os.getenv("GOOGLE_CLOUD_KEY_ID"),
    }
    merged.update({k: v for k, v in config.items() if v is not None})
    return merged


def create_kms_client():
    return kms.KeyManagementServiceClient()
