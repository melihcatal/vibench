# HELPER: speech_client.py
# Provide local configuration and client helper utilities for Streaming Speech-to-Text

import os
import json
from pathlib import Path
import deepgram  # pip install deepgram-sdk-python
import boto3  # pip install boto3
import google.cloud.speech_v1 as speech  # pip install google-cloud-speech
import azure.ai.speech  # pip install azure-ai-speech

# ---------------------------------------------------------------------------
# Helper to select a concrete streaming SDK based on environment variables
# ---------------------------------------------------------------------------


def get_streaming_client(provider: str):
    """Return a configured client object for the selected provider.

    Supported providers and their required env vars:
        - "deepgram"    : DEEPGRAM_API_KEY (WebSocket client via sdk)
        - "aws"         : AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
        - "google"      : GOOGLE_APPLICATION_CREDENTIALS (JSON path)
        - "azure"       : AZURE_SPEECH_KEY, AZURE_SPEECH_REGION
    """
    provider = provider.lower()
    if provider == "deepgram":
        api_key = os.getenv("DEEPGRAM_API_KEY")
        if not api_key:
            raise RuntimeError("Missing DEEPGRAM_API_KEY env var")
        return deepgram.Stream("wss://api.deepgram.io/v1/stream", api_key)
    elif provider == "aws":
        client = boto3.client(
            "transcribe",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        return client
    elif provider == "google":
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise RuntimeError("Missing GOOGLE_APPLICATION_CREDENTIALS env var")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        client = speech.SpeechClient()
        return client
    elif provider == "azure":
        key = os.getenv("AZURE_SPEECH_KEY")
        region = os.getenv("AZURE_SPEECH_REGION", "eastus")
        if not key:
            raise RuntimeError("Missing AZURE_SPEECH_KEY env var")
        return azure.ai.speech.SpeechConfig(key=key, region=region)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


# ---------------------------------------------------------------------------
# Common utilities for payload creation / parsing (provider agnostic)
# ---------------------------------------------------------------------------


def build_stream_config(
    model: str = "nova",
    language: str = "en",
    punctuation: bool = True,
    interim: bool = True,
) -> dict:
    """Create a generic streaming config dict.

    Args:
        model: model identifier (e.g., "nova" for Deepgram; "StreamingRecognitionConfig" model for Google; ...
        language: ISO 639‑1 language code
        punctuation: enable/disable punctuation
        interim: request interim results
    """
    return {
        "model": model,
        "language": language,
        "punctuation": punctuation,
        "interim_results": interim,
    }


def parse_deepgram_result(message: dict):
    """Extract transcript from a Deepgram streaming response message.

    Returns a tuple (transcript: str, is_final: bool)."""
    is_final = message.get("is_final", False)
    alternatives = message.get("alternatives", [])
    transcript = alternatives[0].get("transcript", "") if alternatives else ""
    return transcript, is_final


# ---------------------------------------------------------------------------
# Example usage / entry point (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Just show which helper functions are available
    print("speech_client helpers loaded.")
