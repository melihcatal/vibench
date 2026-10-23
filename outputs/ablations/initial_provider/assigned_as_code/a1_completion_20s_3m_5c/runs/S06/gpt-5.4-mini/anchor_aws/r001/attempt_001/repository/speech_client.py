import os

import boto3


def get_config(config=None):
    data = dict(config or {})
    if "region" not in data:
        data["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if "voice_id" not in data:
        data["voice_id"] = os.getenv("POLLY_VOICE_ID", "Joanna")
    if "output_format" not in data:
        data["output_format"] = os.getenv("POLLY_OUTPUT_FORMAT", "mp3")
    return data


def get_client(config=None):
    cfg = get_config(config)
    return boto3.client("polly", region_name=cfg.get("region"))
