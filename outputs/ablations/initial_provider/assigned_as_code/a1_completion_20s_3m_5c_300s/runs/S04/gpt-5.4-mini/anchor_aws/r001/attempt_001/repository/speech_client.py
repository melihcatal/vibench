import os

import boto3


def load_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "job_name": config.get("job_name"),
        "language_code": config.get("language_code") or os.getenv("AWS_TRANSCRIBE_LANGUAGE_CODE", "en-US"),
        "media_format": config.get("media_format") or "mp3",
        "output_bucket": config.get("output_bucket"),
        "speaker_labels": bool(config.get("speaker_labels", False)),
        "max_speakers": config.get("max_speakers"),
    }


def transcribe_client(config=None):
    config = load_config(config)
    return boto3.client("transcribe", region_name=config["region"])


def s3_client(config=None):
    config = load_config(config)
    return boto3.client("s3", region_name=config["region"])
