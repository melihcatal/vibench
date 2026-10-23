"""Provide local configuration and client helper utilities for Streaming Speech-to-Text.

Uses Google Cloud Speech-to-Text as the backend provider for streaming recognition.
"""

import os
from typing import Dict, Any, Optional

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types as speech_types
from google.api_core import client_options
from google.oauth2 import service_account

# Google Cloud Speech-to-Text default endpoint
GOOGLE_SPEECH_API_ENDPOINT = "speech.googleapis.com"

# Google Cloud Speech-to-Text model identifiers
GOOGLE_SPEECH_MODELS = {
    "default": "default",
    "video": "video",
    "phone_call": "phone_call",
    "command_and_search": "command_and_search",
    "medical_dictation": "medical_dictation",
    "medical_conversation": "medical_conversation",
}

# Supported audio encodings for Google Cloud Speech-to-Text
GOOGLE_AUDIO_ENCODINGS = {
    "linear16": speech_types.RecognitionConfig.AudioEncoding.LINEAR16,
    "flac": speech_types.RecognitionConfig.AudioEncoding.FLAC,
    "mulaw": speech_types.RecognitionConfig.AudioEncoding.MULAW,
    "amr": speech_types.RecognitionConfig.AudioEncoding.AMR,
    "amr_wb": speech_types.RecognitionConfig.AudioEncoding.AMR_WB,
    "ogg_opus": speech_types.RecognitionConfig.AudioEncoding.OGG_OPUS,
    "speex_with_header_byte": speech_types.RecognitionConfig.AudioEncoding.SPEEX_WITH_HEADER_BYTE,
}


def load_google_credentials(credentials_path: Optional[str] = None) -> Optional[service_account.Credentials]:
    """Load Google Cloud service account credentials.

    Args:
        credentials_path: Path to the JSON credentials file. If None, uses
            the GOOGLE_APPLICATION_CREDENTIALS environment variable.

    Returns:
        Service account credentials or None if using default credentials.
    """
    path = credentials_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if path and os.path.exists(path):
        return service_account.Credentials.from_service_account_file(path)
    return None


def get_speech_client(
    credentials_path: Optional[str] = None,
    api_endpoint: Optional[str] = None,
) -> speech.SpeechClient:
    """Create and return a Google Cloud Speech-to-Text client.

    Uses the google-cloud-speech SDK (speech_v1p1beta1) for streaming recognition.

    Args:
        credentials_path: Path to the JSON credentials file.
        api_endpoint: Custom API endpoint (defaults to speech.googleapis.com).

    Returns:
        Configured speech.SpeechClient instance.
    """
    creds = load_google_credentials(credentials_path)
    endpoint = api_endpoint or GOOGLE_SPEECH_API_ENDPOINT

    client_kwargs: Dict[str, Any] = {}
    if creds:
        client_kwargs["credentials"] = creds

    if endpoint and endpoint != GOOGLE_SPEECH_API_ENDPOINT:
        client_kwargs["client_options"] = client_options.ClientOptions(
            api_endpoint=endpoint
        )

    return speech.SpeechClient(**client_kwargs)


def build_streaming_config(
    language_code: str = "en-US",
    encoding: Optional[int] = None,
    sample_rate_hertz: int = 16000,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = False,
    enable_word_confidence: bool = False,
    model: str = "default",
    max_alternatives: int = 1,
    use_enhanced: bool = True,
    profanity_filter: bool = False,
    alternative_language_codes: Optional[list] = None,
) -> speech_types.RecognitionConfig:
    """Build a RecognitionConfig for Google Cloud Speech streaming recognition.

    Args:
        language_code: Primary BCP-47 language code.
        encoding: Audio encoding (default: LINEAR16).
        sample_rate_hertz: Sample rate in Hz.
        enable_automatic_punctuation: Enable auto-punctuation.
        enable_word_time_offsets: Include word timing.
        enable_word_confidence: Include word confidence.
        model: Recognition model identifier.
        max_alternatives: Number of alternative hypotheses.
        use_enhanced: Use enhanced model.
        profanity_filter: Filter profanity.
        alternative_language_codes: Additional languages to recognize.

    Returns:
        Configured RecognitionConfig for use with streaming_recognize.
    """
    if encoding is None:
        encoding = speech_types.RecognitionConfig.AudioEncoding.LINEAR16

    config_kwargs = {
        "language_code": language_code,
        "encoding": encoding,
        "sample_rate_hertz": sample_rate_hertz,
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "enable_word_time_offsets": enable_word_time_offsets,
        "enable_word_confidence": enable_word_confidence,
        "model": model,
        "max_alternatives": max_alternatives,
        "use_enhanced": use_enhanced,
    }

    if profanity_filter:
        config_kwargs["profanity_filter"] = True

    if alternative_language_codes:
        config_kwargs["alternative_language_codes"] = alternative_language_codes

    return speech_types.RecognitionConfig(**config_kwargs)


def get_default_config(language_code: str = "en-US") -> speech_types.RecognitionConfig:
    """Return a default streaming config optimized for microphone input.

    Args:
        language_code: BCP-47 language code.

    Returns:
        Default RecognitionConfig.
    """
    return build_streaming_config(
        language_code=language_code,
        sample_rate_hertz=16000,
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
        model="default",
        use_enhanced=True,
    )
