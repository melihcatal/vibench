import os

import boto3

from security_models import normalize_bytes, normalize_payload, normalize_text


def load_security_config(config=None):
    data = dict(config or {})
    if "region" not in data:
        data["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if "key_id" not in data:
        data["key_id"] = os.getenv("KMS_KEY_ID") or os.getenv("AWS_KMS_KEY_ID")
    if "signing_algorithm" not in data:
        data["signing_algorithm"] = os.getenv("KMS_SIGNING_ALGORITHM", "RSASSA_PSS_SHA_256")
    return data


def kms_client(config=None):
    cfg = load_security_config(config)
    return boto3.client("kms", region_name=cfg.get("region"))


def prepare_payload(payload):
    normalized = normalize_payload(payload)
    normalized["plaintext"] = normalize_bytes(normalized.get("plaintext"))
    normalized["ciphertext"] = normalize_bytes(normalized.get("ciphertext"))
    normalized["message"] = normalize_bytes(normalized.get("message"))
    normalized["text"] = normalize_text(normalized.get("text"))
    return normalized
