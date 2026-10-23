from __future__ import annotations

import os
from functools import lru_cache
from typing import Any


def get_text_to_speech_provider() -> str:
    return os.getenv("TTS_PROVIDER", "google").strip().lower()


@lru_cache(maxsize=1)
def build_client() -> Any:
    provider = get_text_to_speech_provider()
    if provider == "google":
        from google.cloud import texttospeech

        return texttospeech.TextToSpeechClient()
    if provider == "azure":
        import azure.cognitiveservices.speech as speechsdk

        key = os.environ["AZURE_SPEECH_KEY"]
        region = os.environ["AZURE_SPEECH_REGION"]
        speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
        return speech_config
    if provider == "aws":
        import boto3

        return boto3.client("polly", region_name=os.getenv("AWS_REGION"))
    if provider == "openai":
        return os.environ["OPENAI_API_KEY"]
    if provider == "elevenlabs":
        return os.environ["ELEVENLABS_API_KEY"]
    raise RuntimeError(f"Unsupported TTS provider: {provider}")
