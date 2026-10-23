import os
import boto3


def security_config(overrides=None):
    overrides = overrides or {}
    config = {
        "region": overrides.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "key_id": overrides.get("key_id") or os.getenv("AWS_KMS_KEY_ID"),
        "signing_algorithm": overrides.get("signing_algorithm") or os.getenv("AWS_KMS_SIGNING_ALGORITHM", "RSASSA_PSS_SHA_256"),
    }
    config.update({k: v for k, v in overrides.items() if v is not None})
    return config


def kms_client(config=None):
    config = security_config(config)
    return boto3.client("kms", region_name=config.get("region"))
