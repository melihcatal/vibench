import os
from dataclasses import asdict

import boto3

from speech_models import StreamConfig


def load_stream_config() -> StreamConfig:
    return StreamConfig(
        language_code=os.getenv("AWS_TRANSCRIBE_LANGUAGE_CODE", "en-US"),
        enable_punctuation=os.getenv("AWS_TRANSCRIBE_ENABLE_PUNCTUATION", "true").lower() == "true",
        sample_rate_hz=int(os.getenv("AWS_TRANSCRIBE_SAMPLE_RATE_HZ", "16000")),
        encoding=os.getenv("AWS_TRANSCRIBE_ENCODING", "pcm"),
    )


def create_transcribe_client():
    region = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.client("transcribe", region_name=region)


def config_as_headers(config: StreamConfig) -> dict:
    data = asdict(config)
    return {k: str(v) for k, v in data.items()}
