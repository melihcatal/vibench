import os

import boto3


def load_config(config=None):
    merged = dict(config or {})
    if not merged.get("region"):
        merged["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if not merged.get("job_name"):
        merged["job_name"] = os.getenv("AWS_TRANSCRIBE_JOB_NAME")
    return merged


def create_transcribe_client(config=None):
    config = load_config(config)
    return boto3.client("transcribe", region_name=config.get("region"))
