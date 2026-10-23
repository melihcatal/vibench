import os

import boto3


def load_speech_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        "job_name": config.get("job_name"),
        "language_code": config.get("language_code") or "en-US",
        "output_bucket": config.get("output_bucket"),
        "output_key": config.get("output_key"),
    }


def transcribe_client(config=None):
    config = load_speech_config(config)
    return boto3.client("transcribe", region_name=config["region"])


def s3_client(config=None):
    config = load_speech_config(config)
    return boto3.client("s3", region_name=config["region"])
