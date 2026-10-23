import os

import boto3


def load_config(config=None):
    cfg = dict(config or {})
    if "region" not in cfg and os.getenv("AWS_REGION"):
        cfg["region"] = os.getenv("AWS_REGION")
    if "voice_id" not in cfg and os.getenv("POLLY_VOICE_ID"):
        cfg["voice_id"] = os.getenv("POLLY_VOICE_ID")
    if "language_code" not in cfg and os.getenv("POLLY_LANGUAGE_CODE"):
        cfg["language_code"] = os.getenv("POLLY_LANGUAGE_CODE")
    if "output_format" not in cfg and os.getenv("POLLY_OUTPUT_FORMAT"):
        cfg["output_format"] = os.getenv("POLLY_OUTPUT_FORMAT")
    return cfg


def get_client(config=None):
    cfg = load_config(config)
    return boto3.client("polly", region_name=cfg.get("region"))


def stream_to_bytes(stream):
    try:
        return stream.read()
    finally:
        stream.close()
