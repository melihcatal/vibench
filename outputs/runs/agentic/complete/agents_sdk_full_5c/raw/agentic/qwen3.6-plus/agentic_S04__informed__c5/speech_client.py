"""
Local configuration and client helper utilities for Batch Speech-to-Text.

Provides credential loading, client factory, and region/model configuration
for Azure AI Speech batch transcription service.
"""

import os
from typing import Optional, Tuple

from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer


def load_azure_speech_credentials() -> Tuple[str, str]:
    """
    Load Azure AI Speech credentials from environment variables.

    Returns:
        Tuple of (subscription_key, service_region)

    Raises:
        EnvironmentError: If required credentials are not set.
    """
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")

    if not key:
        raise EnvironmentError(
            "AZURE_SPEECH_KEY environment variable is required for Azure AI Speech authentication"
        )
    if not region:
        raise EnvironmentError(
            "AZURE_SPEECH_REGION environment variable is required for Azure AI Speech region"
        )

    return key, region


def create_speech_config(
    subscription_key: Optional[str] = None,
    service_region: Optional[str] = None,
    speech_recognition_language: str = "en-US",
) -> SpeechConfig:
    """
    Create a configured SpeechConfig for Azure AI Speech batch transcription.

    Args:
        subscription_key: Azure Speech subscription key. If None, loaded from AZURE_SPEECH_KEY.
        service_region: Azure Speech service region. If None, loaded from AZURE_SPEECH_REGION.
        speech_recognition_language: Language locale for recognition (default: en-US).

    Returns:
        Configured SpeechConfig instance.
    """
    if subscription_key is None or service_region is None:
        subscription_key, service_region = load_azure_speech_credentials()

    config = SpeechConfig(subscription=subscription_key, region=service_region)
    config.speech_recognition_language = speech_recognition_language

    return config


def get_supported_models() -> dict:
    """
    Return supported Azure AI Speech batch transcription models and their IDs.

    Returns:
        Dictionary mapping model names to their Azure Speech model identifiers.
    """
    return {
        "base": "Microsoft.BaseRecognizer",
        "conversational": "Microsoft.ConversationalRecognizer",
        "telephony": "Microsoft.TelephonyRecognizer",
        "medical": "Microsoft.MedicalRecognizer",
        "en-us-base": "en-US-Baseline",
        "en-us-conversational": "en-US-ConversationalRecognizer",
        "en-us-telephony": "en-US-TelephonyRecognizer",
    }


def get_default_batch_endpoint(region: Optional[str] = None) -> str:
    """
    Construct the Azure AI Speech batch transcription REST endpoint URL.

    The batch transcription API requires REST calls even when using the SDK
    for real-time recognition.

    Args:
        region: Azure region string. If None, loaded from AZURE_SPEECH_REGION.

    Returns:
        Base URL for the Azure Speech batch transcription API.
    """
    if region is None:
        _, region = load_azure_speech_credentials()

    return f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.1"


def build_transcription_payload(
    audio_uri: str,
    locale: str = "en-US",
    display_name: str = "batch_transcription",
    model_id: Optional[str] = None,
    diarization_enabled: bool = False,
    word_level_timestamps: bool = True,
    punctuation_mode: str = "dictated_and_automatic",
) -> dict:
    """
    Build the JSON payload for Azure AI Speech batch transcription submission.

    Args:
        audio_uri: SAS or accessible URI to the audio file.
        locale: Language locale (default: en-US).
        display_name: Display name for the transcription job.
        model_id: Specific Azure Speech model ID. Uses base if None.
        diarization_enabled: Enable speaker diarization.
        word_level_timestamps: Include word-level timestamps.
        punctuation_mode: Punctuation mode for output.

    Returns:
        Dictionary suitable for JSON serialization to the Azure Speech batch API.
    """
    models = []
    if model_id:
        models.append({"id": model_id})

    properties = {
        "diarizationEnabled": diarization_enabled,
        "wordLevelTimestampsEnabled": word_level_timestamps,
        "punctuationMode": punctuation_mode,
        "profanityFilterMode": "masked",
    }

    payload = {
        "displayName": display_name,
        "locale": locale,
        "recordingsUrl": audio_uri,
        "properties": properties,
    }

    if models:
        payload["models"] = models

    return payload
