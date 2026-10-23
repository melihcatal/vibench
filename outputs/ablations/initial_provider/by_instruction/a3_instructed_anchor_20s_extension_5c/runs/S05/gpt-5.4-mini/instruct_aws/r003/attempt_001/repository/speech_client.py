import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass
class SpeechConfig:
    region_name: str
    language_code: str
    media_sample_rate_hz: int
    media_encoding: str
    punctuation: bool


def load_speech_config(language_code: Optional[str] = None, punctuation: Optional[bool] = None) -> SpeechConfig:
    region_name = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    return SpeechConfig(
        region_name=region_name,
        language_code=language_code or os.environ.get("AWS_TRANSCRIBE_LANGUAGE_CODE", "en-US"),
        media_sample_rate_hz=int(os.environ.get("AWS_TRANSCRIBE_SAMPLE_RATE_HZ", "16000")),
        media_encoding=os.environ.get("AWS_TRANSCRIBE_MEDIA_ENCODING", "pcm"),
        punctuation=punctuation if punctuation is not None else os.environ.get("AWS_TRANSCRIBE_PUNCTUATION", "true").lower() == "true",
    )


def make_transcribe_streaming_client(region_name: str):
    return boto3.client("transcribe", region_name=region_name)


def make_bedrock_runtime_client(region_name: str):
    return boto3.client("bedrock-runtime", region_name=region_name)
