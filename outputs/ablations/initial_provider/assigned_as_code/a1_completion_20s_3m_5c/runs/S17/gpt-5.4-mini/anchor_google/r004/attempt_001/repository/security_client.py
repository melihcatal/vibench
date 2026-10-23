import os

from google.cloud import kms


def load_config(config=None):
    merged = dict(config or {})
    merged.setdefault("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT", ""))
    merged.setdefault("location", os.environ.get("GOOGLE_CLOUD_LOCATION", "global"))
    merged.setdefault("key_ring", os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING", ""))
    merged.setdefault("key_id", os.environ.get("GOOGLE_CLOUD_KMS_KEY_ID", ""))
    merged.setdefault("key_name", os.environ.get("GOOGLE_CLOUD_KMS_KEY_NAME", ""))
    merged.setdefault("signature_key_version", os.environ.get("GOOGLE_CLOUD_KMS_KEY_VERSION", "1"))
    return merged


def kms_client():
    return kms.KeyManagementServiceClient()


def crypto_key_path(config):
    client = kms_client()
    if config.get("key_name"):
        return config["key_name"]
    return client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])


def crypto_key_version_path(config):
    client = kms_client()
    return client.crypto_key_version_path(config["project_id"], config["location"], config["key_ring"], config["key_id"], config.get("signature_key_version", "1"))
