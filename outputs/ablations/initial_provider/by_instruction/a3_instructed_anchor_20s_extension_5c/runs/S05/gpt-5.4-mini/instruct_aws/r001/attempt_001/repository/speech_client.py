import os
from dataclasses import asdict
from typing import Any, Dict

import boto3

from speech_models import StreamingSpeechConfig


def load_streaming_speech_config() -> StreamingSpeechConfig:
    return StreamingSpeechConfig(
        region=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        language_code=os.environ.get("AWS_TRANSCRIBE_LANGUAGE_CODE", "en-US"),
        sample_rate_hz=int(os.environ.get("AWS_TRANSCRIBE_SAMPLE_RATE_HZ", "16000")),
        media_encoding=os.environ.get("AWS_TRANSCRIBE_MEDIA_ENCODING", "pcm"),
        enable_partial_results=os.environ.get("AWS_TRANSCRIBE_ENABLE_PARTIAL_RESULTS", "true").lower() == "true",
        enable_punctuation=os.environ.get("AWS_TRANSCRIBE_ENABLE_PUNCTUATION", "true").lower() == "true",
    )


def build_transcribe_stream_client(region: str | None = None):
    session = boto3.session.Session(region_name=region or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))
    return session.client("transcribe-streaming")


def config_to_request_kwargs(config: StreamingSpeechConfig) -> Dict[str, Any]:
    data = asdict(config)
    return {
        "language_code": data["language_code"],
        "media_sample_rate_hz": data["sample_rate_hz"],
        "media_encoding": data["media_encoding"],
        "enable_partial_results_stabilization": data["enable_partial_results"],
        "show_speaker_label": False,
        "enable_partial_results": data["enable_partial_results"],
        "language_model_name": None,
        "vocabulary_name": None,
        "identify_language": False,
        "enable_channel_identification": False,
        "number_of_channels": 1,
        "enable_partial_results_stabilization": data["enable_partial_results"],
        "enable_language_id": False,
        "enable_partial_results": data["enable_partial_results"],
        "content_identification_type": "PII",
        "enable_partial_results_stabilization": data["enable_partial_results"],
        "language_code": data["language_code"],
        "show_speaker_label": False,
        "enable_partial_results": data["enable_partial_results"],
        "enable_partial_results_stabilization": data["enable_partial_results"],
        "x_amzn_transcribe_punctuation_enabled": data["enable_punctuation"],
    }
