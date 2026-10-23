import os

import boto3
from amazon_transcribe.client import TranscribeStreamingClient

from speech_models import StreamingSpeechConfig, normalize_language_code


def load_streaming_speech_config(payload=None, config=None):
    payload = payload or {}
    config = config or {}
    return StreamingSpeechConfig(
        region=config.get("region") or os.getenv("AWS_REGION") or boto3.Session().region_name or "us-east-1",
        language_code=normalize_language_code(payload.get("language_code") or config.get("language_code")),
        sample_rate_hz=int(payload.get("sample_rate_hz") or config.get("sample_rate_hz") or 16000),
        media_encoding=(payload.get("media_encoding") or config.get("media_encoding") or "pcm"),
        enable_partial_results_stabilization=bool(config.get("enable_partial_results_stabilization", True)),
        show_speaker_label=bool(config.get("show_speaker_label", False)),
        enable_punctuation=bool(config.get("enable_punctuation", True)),
    )


def create_transcribe_client(config=None):
    config = config or {}
    return TranscribeStreamingClient(region=config.get("region") or boto3.Session().region_name or "us-east-1")
