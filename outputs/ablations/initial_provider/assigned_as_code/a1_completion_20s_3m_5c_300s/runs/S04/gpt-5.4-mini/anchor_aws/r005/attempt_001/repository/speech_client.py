import os

import boto3


def load_speech_config(config=None):
    base = {
        "region": os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "bucket": os.getenv("AWS_S3_BUCKET"),
    }
    merged = dict(base)
    if config:
        merged.update({k: v for k, v in config.items() if v is not None})
    return merged


def get_transcribe_client(config=None):
    cfg = load_speech_config(config)
    return boto3.client("transcribe", region_name=cfg.get("region"))


def get_s3_client(config=None):
    cfg = load_speech_config(config)
    return boto3.client("s3", region_name=cfg.get("region"))


def normalize_media_uri(payload, config=None):
    cfg = load_speech_config(config)
    audio_uri = payload.get("audio_uri") or payload.get("media_uri")
    if audio_uri:
        return audio_uri
    bucket = cfg.get("bucket")
    key = payload.get("audio_key") or payload.get("key")
    if bucket and key:
        return f"s3://{bucket}/{key}"
    raise ValueError("audio_uri or S3 bucket/key required")
