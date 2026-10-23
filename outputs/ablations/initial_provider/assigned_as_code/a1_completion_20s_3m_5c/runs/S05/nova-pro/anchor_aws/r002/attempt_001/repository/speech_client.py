import boto3

from amazon_transcribe.client import TranscribeStreamingClient

def get_speech_client(region=None):
    return TranscribeStreamingClient(region=region or boto3.Session().region_name or "us-east-1")

def normalize_payload(payload):
    return {
        "language_code": payload.get("language_code", "en-US"),
        "sample_rate_hz": payload.get("sample_rate_hz", 16000),
        "audio_chunks": payload.get("audio_chunks", [])
    }