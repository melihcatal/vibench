import os
import deepgram
import boto3
from google.cloud import speech_v1p1beta1 as speech


class SpeechClient:
    """Helper utilities for Streaming Speech-to-Text using multiple providers."""

    # ---- DEEPGRAM (Streaming API) ----
    def __init__(self, deepgram_api_key: str = None):
        self.deepgram = None
        if deepgram_api_key:
            self.deepgram = deepgram.Deepgram(deepgram_api_key)
        elif os.getenv("DEEPGRAM_API_KEY"):
            self.deepgram = deepgram.Deepgram(os.getenv("DEEPGRAM_API_KEY"))
        else:
            raise ValueError(
                "Deepgram API key not provided. Set via constructor or DEEPGRAM_API_KEY env var."
            )

    # ---- Amazon Transcribe Streaming ----
    def __init_amazon(self, aws_access_key: str = None, aws_secret_key: str = None):
        if aws_access_key and aws_secret_key:
            self.transcribe = boto3.client(
                "transcribe",
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
            )
        else:
            self.transcribe = boto3.client("transcribe")

    # ---- Google Cloud Speech (v1p1beta1) ----
    def __init_google(self, credentials_path: str = None):
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            raise ValueError(
                "Google credentials path not set. Provide via argument or env var."
            )
        self.speech_client = speech.SpeechClient()

    # Factory method to create provider-specific client
    @classmethod
    def create(cls, provider: str = "deepgram", **kwargs):
        if provider == "deepgram":
            return cls(deepgram_api_key=kwargs.get("deepgram_api_key"))
        elif provider == "amazon":
            return cls(
                aws_access_key=kwargs.get("aws_access_key_id"),
                aws_secret_key=kwargs.get("aws_secret_access_key"),
            )
        elif provider == "google":
            return cls(credentials_path=kwargs.get("credentials_path"))
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    # Generic streaming method (implementation per provider)
    async def stream_audio(self, audio_stream):
        raise NotImplementedError("Subclasses must implement stream_audio")


# Example usage (not executed)
# if __name__ == "__main__":
#     client = SpeechClient.create(provider="deepgram", deepgram_api_key="sk_..." )
#     # ... use client to stream audio via client.stream_audio()
