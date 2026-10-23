import os
from dataclasses import dataclass

import boto3


@dataclass
class SpeechConfig:
    region: str | None = None
    voice_id: str | None = None
    output_format: str = "mp3"


def load_config(config=None):
    config = config or {}
    return SpeechConfig(
        region=config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        voice_id=config.get("voice_id") or os.getenv("POLLY_VOICE_ID", "Joanna"),
        output_format=config.get("output_format", "mp3"),
    )


def client(config=None):
    cfg = load_config(config)
    return boto3.client("polly", region_name=cfg.region)
