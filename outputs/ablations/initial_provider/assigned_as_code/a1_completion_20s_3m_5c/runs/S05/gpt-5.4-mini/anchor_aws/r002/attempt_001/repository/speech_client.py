import os

import boto3
from amazon_transcribe.client import TranscribeStreamingClient


def speech_region(config=None):
    config = config or {}
    return config.get("region") or os.getenv("AWS_REGION") or boto3.Session().region_name or "us-east-1"


def transcribe_streaming_client(config=None):
    return TranscribeStreamingClient(region=speech_region(config))


def bedrock_runtime_client(config=None):
    config = config or {}
    return boto3.client("bedrock-runtime", region_name=config.get("region") or os.getenv("AWS_REGION") or boto3.Session().region_name or "us-east-1")


def transcribe_start_args(payload, config=None):
    config = config or {}
    args = {
        "language_code": payload["language_code"],
        "media_sample_rate_hz": payload["sample_rate_hz"],
        "media_encoding": "pcm",
    }
    if config.get("language_model_name"):
        args["vocabulary_name"] = config["language_model_name"]
    return args
