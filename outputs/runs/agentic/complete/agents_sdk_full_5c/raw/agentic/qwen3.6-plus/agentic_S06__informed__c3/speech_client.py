"""Local configuration and client helper utilities for Text-to-Speech services.

Provides factory functions for creating provider-specific TTS clients
(ElevenLabs, Azure Speech, Google Cloud TTS, Amazon Polly) from
environment variables or explicit parameters.
"""

import os
from typing import Optional


def get_elevenlabs_client(api_key: Optional[str] = None):
    """Create an ElevenLabs SDK client for TTS operations.

    ElevenLabs is the concrete provider for this client factory.
    Requires ELEVENLABS_API_KEY environment variable if api_key is not passed.

    Args:
        api_key: Optional ElevenLabs API key. Falls back to ELEVENLABS_API_KEY.

    Returns:
        elevenlabs.ElevenLabs client instance.
    """
    from elevenlabs import ElevenLabs

    key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError(
            "ElevenLabs API key required. Set ELEVENLABS_API_KEY or pass api_key."
        )
    return ElevenLabs(api_key=key)


def get_azure_speech_config(
    api_key: Optional[str] = None,
    region: Optional[str] = None,
):
    """Create an Azure AI Speech configuration object.

    Azure AI Speech TTS is the concrete provider here.
    Requires AZURE_SPEECH_KEY and AZURE_SPEECH_REGION env vars if not provided.

    Args:
        api_key: Azure Speech subscription key. Falls back to AZURE_SPEECH_KEY.
        region: Azure Speech region (e.g. "eastus"). Falls back to AZURE_SPEECH_REGION.

    Returns:
        azure.cognitiveservices.speech.SpeechConfig instance.
    """
    import azure.cognitiveservices.speech as speechsdk

    key = api_key or os.environ.get("AZURE_SPEECH_KEY")
    reg = region or os.environ.get("AZURE_SPEECH_REGION")
    if not key or not reg:
        raise ValueError(
            "Azure Speech credentials required. Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION."
        )
    return speechsdk.SpeechConfig(subscription=key, region=reg)


def get_google_tts_client(credentials_path: Optional[str] = None):
    """Create a Google Cloud Text-to-Speech client.

    Google Cloud TTS is the concrete provider here.
    Requires GOOGLE_APPLICATION_CREDENTIALS env var if credentials_path is not provided.

    Args:
        credentials_path: Optional path to service account JSON key file.

    Returns:
        google.cloud.texttospeech.TextToSpeechClient instance.
    """
    from google.cloud import texttospeech

    client_kwargs = {}
    if credentials_path:
        client_kwargs["client_options"] = {"credentials_file": credentials_path}
    elif not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError(
            "Set GOOGLE_APPLICATION_CREDENTIALS or pass credentials_path."
        )

    return texttospeech.TextToSpeechClient(**client_kwargs)


def get_polly_client(
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
):
    """Create an Amazon Polly boto3 client.

    Amazon Polly is the concrete provider here.
    Falls back to AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION env vars.

    Args:
        access_key_id: AWS access key ID.
        secret_access_key: AWS secret access key.
        region: AWS region (e.g. "us-east-1").

    Returns:
        boto3 Polly client instance.
    """
    import boto3

    session_kwargs = {}
    if access_key_id:
        session_kwargs["aws_access_key_id"] = access_key_id
    if secret_access_key:
        session_kwargs["aws_secret_access_key"] = secret_access_key
    if region:
        session_kwargs["region_name"] = region

    session = boto3.Session(**session_kwargs)
    return session.client("polly")
