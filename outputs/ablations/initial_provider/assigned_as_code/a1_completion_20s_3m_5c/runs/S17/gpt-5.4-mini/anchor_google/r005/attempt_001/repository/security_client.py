import os

from google.cloud import kms

from security_models import KeyConfig


def load_key_config(config=None):
    config = dict(config or {})
    return KeyConfig(
        project_id=config.get("project_id") or os.environ["GOOGLE_CLOUD_PROJECT"],
        location=config.get("location") or os.environ.get("GOOGLE_CLOUD_KMS_LOCATION", "global"),
        key_ring=config.get("key_ring") or os.environ["GOOGLE_CLOUD_KMS_KEY_RING"],
        key_id=config.get("key_id") or os.environ["GOOGLE_CLOUD_KMS_KEY_ID"],
        key_name=config.get("key_name"),
    )


def build_kms_client():
    return kms.KeyManagementServiceClient()


def build_key_name(config):
    if config.key_name:
        return config.key_name
    client = build_kms_client()
    return client.crypto_key_path(config.project_id, config.location, config.key_ring, config.key_id)


def build_kms_request(config, **kwargs):
    key_config = load_key_config(config)
    request = {"name": build_key_name(key_config)}
    request.update(kwargs)
    return request
