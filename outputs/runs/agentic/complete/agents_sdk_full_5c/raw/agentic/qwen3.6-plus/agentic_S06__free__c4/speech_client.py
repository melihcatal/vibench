"""
speech_client.py - Local configuration and client helper utilities for Text-to-Speech.

Provides Azure Cognitive Services Speech SDK configuration,
client initialization, and helper utilities for TTS operations.
"""

import os
from typing import Optional

# Azure Speech Services configuration
AZURE_SPEECH_REGION = os.environ.get("AZURE_SPEECH_REGION", "eastus")
AZURE_SPEECH_KEY = os.environ.get("AZURE_SPEECH_KEY", "")
AZURE_SPEECH_ENDPOINT = os.environ.get(
    "AZURE_SPEECH_ENDPOINT",
    f"https://{AZURE_SPEECH_REGION}.tts.speech.microsoft.com/",
)

# Supported Azure voice locales
SUPPORTED_LOCALES = {
    "en-US": ["en-US-AriaNeural", "en-US-GuyNeural", "en-US-JennyNeural", "en-US-DavisNeural"],
    "en-GB": ["en-GB-SoniaNeural", "en-GB-RyanNeural"],
    "fr-FR": ["fr-FR-DeniseNeural", "fr-FR-HenriNeural"],
    "de-DE": ["de-DE-KatjaNeural", "de-DE-ConradNeural"],
    "es-ES": ["es-ES-ElviraNeural", "es-ES-AlvaroNeural"],
    "ja-JP": ["ja-JP-NanamiNeural", "ja-JP-KeitaNeural"],
    "zh-CN": ["zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural"],
    "pt-BR": ["pt-BR-FranciscaNeural", "pt-BR-AntonioNeural"],
}

# Azure output audio formats
AUDIO_FORMATS = {
    "mp3": "audio-16khz-32kbitrate-mono-mp3",
    "wav": "riff-16khz-16bit-mono-pcm",
    "ogg": "ogg-16khz-16bit-mono-opus",
    "flac": "flac-16khz-16bit-mono",
}


def get_speech_config(
    region: Optional[str] = None,
    subscription_key: Optional[str] = None,
) -> dict:
    """
    Build Azure Speech Services configuration dictionary.

    Args:
        region: Azure region (defaults to AZURE_SPEECH_REGION env var).
        subscription_key: Azure subscription key (defaults to AZURE_SPEECH_KEY env var).

    Returns:
        Configuration dictionary for Azure Speech SDK.
    """
    return {
        "region": region or AZURE_SPEECH_REGION,
        "subscription_key": subscription_key or AZURE_SPEECH_KEY,
        "endpoint": AZURE_SPEECH_ENDPOINT,
        "service_host": f"{region or AZURE_SPEECH_REGION}.tts.speech.microsoft.com",
    }


def get_rest_api_headers(subscription_key: Optional[str] = None) -> dict:
    """
    Build HTTP headers for Azure TTS REST API calls.

    Uses the Ocp-Apim-Subscription-Key header pattern required by
    https://{region}.tts.speech.microsoft.com/cognitiveservices/v1

    Args:
        subscription_key: Azure subscription key.

    Returns:
        Dictionary of HTTP headers for Azure TTS REST API.
    """
    key = subscription_key or AZURE_SPEECH_KEY
    return {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/ssml+xml",
        "User-Agent": "AzureTTSServiceIntegration/1.0",
        "X-Microsoft-OutputFormat": AUDIO_FORMATS["mp3"],
    }


def build_tts_endpoint(region: Optional[str] = None) -> str:
    """
    Construct the Azure TTS REST synthesis endpoint URL.

    Args:
        region: Azure region for the endpoint.

    Returns:
        Full endpoint URL for Azure Cognitive Services TTS REST API.
    """
    r = region or AZURE_SPEECH_REGION
    return f"https://{r}.tts.speech.microsoft.com/cognitiveservices/v1"


def validate_azure_credentials(region: Optional[str] = None, key: Optional[str] = None) -> bool:
    """
    Validate that Azure Speech credentials are configured.

    Args:
        region: Azure region to validate.
        key: Subscription key to validate.

    Returns:
        True if credentials appear valid, False otherwise.
    """
    r = region or AZURE_SPEECH_REGION
    k = key or AZURE_SPEECH_KEY
    return bool(r and k and len(k) > 10)
