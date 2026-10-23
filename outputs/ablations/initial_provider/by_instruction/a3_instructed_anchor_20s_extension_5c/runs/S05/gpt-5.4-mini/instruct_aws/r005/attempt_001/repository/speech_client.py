import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass
class SpeechConfig:
    region_name: str
    language_code: str = "en-US"
    sample_rate_hz: int = 16000
    media_encoding: str = "pcm"
    enable_partial_results_stabilization: bool = True
    partial_results_stability: str = "high"
    show_speaker_label: bool = False
    vocabulary_name: Optional[str] = None


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        region_name=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        language_code=os.environ.get("AWS_TRANSCRIBE_LANGUAGE_CODE", "en-US"),
        sample_rate_hz=int(os.environ.get("AWS_TRANSCRIBE_SAMPLE_RATE", "16000")),
        media_encoding=os.environ.get("AWS_TRANSCRIBE_MEDIA_ENCODING", "pcm"),
    )


def create_transcribe_client(region_name: Optional[str] = None):
    return boto3.client("transcribe", region_name=region_name or load_speech_config().region_name)


def create_transcribe_streaming_client(region_name: Optional[str] = None):
    return boto3.client("transcribe-streaming", region_name=region_name or load_speech_config().region_name)
