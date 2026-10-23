import os
from typing import Any, Dict

import boto3
from amazon_transcribe.client import TranscribeStreamingClient

from speech_models import StreamingSpeechRequest


def load_speech_config(config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    data = dict(config or {})
    data.setdefault("region", os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1")
    data.setdefault("language_code", os.environ.get("AWS_TRANSCRIBE_LANGUAGE_CODE") or "en-US")
    data.setdefault("sample_rate_hz", int(os.environ.get("AWS_TRANSCRIBE_SAMPLE_RATE_HZ") or 16000))
    data.setdefault("enable_punctuation", os.environ.get("AWS_TRANSCRIBE_ENABLE_PUNCTUATION", "true").lower() == "true")
    return data


def build_transcribe_client(config: Dict[str, Any] | None = None) -> TranscribeStreamingClient:
    data = load_speech_config(config)
    return TranscribeStreamingClient(region=data["region"] or boto3.Session().region_name or "us-east-1")


def build_streaming_request(payload: Dict[str, Any]) -> StreamingSpeechRequest:
    return StreamingSpeechRequest(
        audio_chunks=list(payload.get("audio_chunks") or []),
        language_code=payload.get("language_code") or "en-US",
        sample_rate_hz=int(payload.get("sample_rate_hz") or 16000),
        enable_punctuation=bool(payload.get("enable_punctuation", True)),
    )
