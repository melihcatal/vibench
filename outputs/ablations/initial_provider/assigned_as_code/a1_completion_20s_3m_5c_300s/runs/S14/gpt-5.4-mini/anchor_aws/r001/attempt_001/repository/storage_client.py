import os

import boto3

from storage_models import normalize_config


def load_storage_config(config=None):
    merged = dict(config or {})
    if not merged.get("region"):
        merged["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if not merged.get("bucket"):
        merged["bucket"] = os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET")
    if not merged.get("prefix"):
        merged["prefix"] = os.getenv("S3_PREFIX", "")
    if not merged.get("expires_in"):
        merged["expires_in"] = os.getenv("S3_URL_EXPIRES_IN", "3600")
    return normalize_config(merged)


def get_s3_client(config=None):
    cfg = load_storage_config(config)
    return boto3.client("s3", region_name=cfg["region"]), cfg
