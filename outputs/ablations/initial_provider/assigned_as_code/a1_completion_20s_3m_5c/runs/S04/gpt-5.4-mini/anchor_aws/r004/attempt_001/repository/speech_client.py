import os

import boto3


def load_speech_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "job_name": config.get("job_name") or os.getenv("AWS_TRANSCRIBE_JOB_NAME"),
        "output_bucket": config.get("output_bucket") or os.getenv("AWS_TRANSCRIBE_OUTPUT_BUCKET"),
    }


def get_transcribe_client(config=None):
    cfg = load_speech_config(config)
    return boto3.client("transcribe", region_name=cfg["region"])


def get_s3_client(config=None):
    cfg = load_speech_config(config)
    return boto3.client("s3", region_name=cfg["region"])
