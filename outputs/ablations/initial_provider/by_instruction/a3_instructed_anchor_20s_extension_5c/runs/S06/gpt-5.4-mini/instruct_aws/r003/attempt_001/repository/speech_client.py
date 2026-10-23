import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3


@dataclass
class SpeechClientConfig:
    region_name: str
    default_voice_id: Optional[str]
    default_output_format: str


@lru_cache(maxsize=1)
def load_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        region_name=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        default_voice_id=os.environ.get("AWS_POLLY_VOICE_ID"),
        default_output_format=os.environ.get("AWS_POLLY_OUTPUT_FORMAT", "mp3"),
    )


def create_polly_client():
    config = load_config()
    return boto3.client("polly", region_name=config.region_name)


def resolve_voice_id(voice_id: Optional[str] = None) -> Optional[str]:
    return voice_id or load_config().default_voice_id


def resolve_output_format(output_format: Optional[str] = None) -> str:
    return output_format or load_config().default_output_format
