"""
Submit an audio file for batch transcription using Azure AI Speech.

Uses the Azure AI Speech batch transcription REST API (v3.1) to create
a new transcription job from an audio file accessible via URI.
"""

import os
import json
from typing import Optional, Dict

import requests

from speech_client import (
    load_azure_speech_credentials,
    build_transcription_payload,
    get_default_batch_endpoint,
    get_supported_models,
)


def submit_transcription(
    audio_uri: str,
    locale: str = "en-US",
    display_name: str = "batch_transcription",
    model_id: Optional[str] = None,
    diarization_enabled: bool = False,
    word_level_timestamps: bool = True,
) -> str:
    """
    Submit an audio file for batch transcription via Azure AI Speech REST API.

    The audio file must be accessible via a URI (e.g., Azure Blob SAS URL).
    Azure AI Speech processes the file asynchronously and returns a job ID
    that can be used to poll for results.

    Args:
        audio_uri: SAS or public URL pointing to the audio file.
        locale: Language/locale for speech recognition (default: en-US).
        display_name: Human-readable name for the transcription job.
        model_id: Optional Azure Speech model ID (e.g., 'en-US-ConversationalRecognizer').
        diarization_enabled: Whether to enable speaker diarization.
        word_level_timestamps: Whether to include word-level timing.

    Returns:
        The transcription job ID (str) returned by Azure AI Speech.

    Raises:
        requests.HTTPError: If the Azure API returns an error response.
        EnvironmentError: If AZURE_SPEECH_KEY or AZURE_SPEECH_REGION is not set.
    """
    key, region = load_azure_speech_credentials()

    endpoint = f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    payload = build_transcription_payload(
        audio_uri=audio_uri,
        locale=locale,
        display_name=display_name,
        model_id=model_id,
        diarization_enabled=diarization_enabled,
        word_level_timestamps=word_level_timestamps,
    )

    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()

    location_url = response.headers.get("location", "")
    transcription_id = location_url.rstrip("/").split("/")[-1]

    return transcription_id


def submit_with_custom_properties(
    audio_uri: str,
    locale: str = "en-US",
    display_name: str = "batch_transcription",
    custom_properties: Optional[Dict] = None,
) -> str:
    """
    Submit a transcription job with custom Azure AI Speech properties.

    Allows full control over the Azure Speech batch transcription request
    including custom model adaptations, profanity filtering, and output formats.

    Args:
        audio_uri: Accessible URI to the audio file.
        locale: Language locale (default: en-US).
        display_name: Job display name.
        custom_properties: Optional dict of additional Azure Speech properties
            to merge into the request (e.g., custom acoustic model IDs).

    Returns:
        The transcription job ID.
    """
    key, region = load_azure_speech_credentials()
    endpoint = f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    base_properties = {
        "diarizationEnabled": False,
        "wordLevelTimestampsEnabled": True,
        "punctuationMode": "dictated_and_automatic",
        "profanityFilterMode": "masked",
    }

    if custom_properties:
        base_properties.update(custom_properties)

    payload = {
        "displayName": display_name,
        "locale": locale,
        "recordingsUrl": audio_uri,
        "properties": base_properties,
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()

    location_url = response.headers.get("location", "")
    transcription_id = location_url.rstrip("/").split("/")[-1]

    return transcription_id
