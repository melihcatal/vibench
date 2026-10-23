import os
import boto3


def load_security_config(config=None):
    config = config or {}
    merged = {
        "region": config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "key_id": config.get("key_id") or os.getenv("AWS_KMS_KEY_ID"),
        "signing_algorithm": config.get("signing_algorithm") or os.getenv("AWS_KMS_SIGNING_ALGORITHM"),
    }
    merged.update({k: v for k, v in config.items() if v is not None})
    return merged


def kms_client(config=None):
    cfg = load_security_config(config)
    return boto3.client("kms", region_name=cfg.get("region"))
