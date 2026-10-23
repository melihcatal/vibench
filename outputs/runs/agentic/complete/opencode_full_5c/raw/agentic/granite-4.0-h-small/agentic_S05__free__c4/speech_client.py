# [HELPER] speech_client.py
"""Local configuration and client utilities for Google Cloud Streaming Speech-to-Text."""

import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

# Automatically select the default service account credentials from the environment
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/tmp/vibench_agentic/20260418_123707_vibench_agentic_opencode_env_ablation_3c/granite-4.0-h-small/agentic_S05__free__c4/key.json"
)

# Helper to create a Speech client with common defaults


def get_speech_client() -> speech.SpeechClient:
    """Create and return a configured Speech client."""
    return speech.SpeechClient()


# Pre‑defined audio encoding constants for reuse
AudioEncoding = speech.RecognitionConfig.AudioEncoding

# Helper for common recognition configs (used in other modules)


def get_base_recognition_config() -> speech.RecognitionConfig:
    """Return a base recognition config used by streaming modules."""
    return speech.RecognitionConfig(
        encoding=AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )


if __name__ == "__main__":
    # Quick demo – print the client’s project ID
    client = get_speech_client()
    print("Using project:", client.project)
