import os

from google.cloud import kms


def load_security_config(config=None):
    config = dict(config or {})
    config.setdefault("project_id", os.getenv("GOOGLE_CLOUD_PROJECT", ""))
    config.setdefault("location", os.getenv("GOOGLE_CLOUD_LOCATION", "global"))
    config.setdefault("key_ring", os.getenv("GOOGLE_CLOUD_KMS_KEY_RING", ""))
    config.setdefault("key_id", os.getenv("GOOGLE_CLOUD_KMS_KEY_ID", ""))
    config.setdefault("bucket", os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", ""))
    return config


def build_kms_client():
    return kms.KeyManagementServiceClient()
