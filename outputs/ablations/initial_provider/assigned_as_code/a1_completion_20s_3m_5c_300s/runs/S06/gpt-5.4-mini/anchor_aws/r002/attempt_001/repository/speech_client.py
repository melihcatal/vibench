import os

import boto3


def load_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "voice_id": config.get("voice_id") or os.getenv("POLLY_VOICE_ID", "Joanna"),
        "output_format": config.get("output_format") or os.getenv("POLLY_OUTPUT_FORMAT", "mp3"),
        "language_code": config.get("language_code") or os.getenv("POLLY_LANGUAGE_CODE"),
        "sample_rate": config.get("sample_rate") or os.getenv("POLLY_SAMPLE_RATE"),
    }


def get_client(config=None):
    cfg = load_config(config)
    return boto3.client("polly", region_name=cfg["region"])
