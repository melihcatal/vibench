import os

import boto3
from amazon_transcribe.client import TranscribeStreamingClient

from speech_models import AudioChunkStreamRequest


def get_region(config=None):
    config = config or {}
    return config.get("region") or os.getenv("AWS_REGION") or boto3.Session().region_name or "us-east-1"


def create_transcribe_client(config=None):
    return TranscribeStreamingClient(region=get_region(config))


def build_stream_request(payload, config=None):
    config = config or {}
    if isinstance(payload, AudioChunkStreamRequest):
        return payload
    return AudioChunkStreamRequest(
        audio_chunks=payload["audio_chunks"],
        language_code=payload.get("language_code", config.get("language_code", "en-US")),
        sample_rate_hz=payload.get("sample_rate_hz", config.get("sample_rate_hz", 16000)),
        show_speaker_label=payload.get("show_speaker_label", config.get("show_speaker_label", False)),
        enable_partial_results_stabilization=payload.get("enable_partial_results_stabilization", config.get("enable_partial_results_stabilization", True)),
        enable_channel_identification=payload.get("enable_channel_identification", config.get("enable_channel_identification", False)),
        vocabulary_name=payload.get("vocabulary_name", config.get("vocabulary_name")),
        model_name=payload.get("model_name", config.get("model_name")),
    )
