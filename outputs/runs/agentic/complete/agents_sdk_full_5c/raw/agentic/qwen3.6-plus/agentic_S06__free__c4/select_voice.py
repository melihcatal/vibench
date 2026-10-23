"""
select_voice.py - Lists or selects a voice for a target locale.

Uses Azure Cognitive Services Speech Service REST API to retrieve
available neural voices and select the best match for a target locale.
Provider: Microsoft Azure Cognitive Services Speech Service
Endpoint: https://{region}.tts.speech.microsoft.com/cognitiveservices/voices/list
"""

import requests
from typing import Optional, List

from speech_client import (
    build_tts_endpoint,
    validate_azure_credentials,
    AZURE_SPEECH_KEY,
    AZURE_SPEECH_REGION,
    SUPPORTED_LOCALES,
)
from speech_models import VoiceInfo, parse_azure_voice_list_response, normalize_locale


def list_voices(
    region: Optional[str] = None,
    subscription_key: Optional[str] = None,
    locale_filter: Optional[str] = None,
) -> List[VoiceInfo]:
    """
    List available voices from Azure Cognitive Services Speech Service.

    Calls the Azure /cognitiveservices/voices/list REST API endpoint
    to retrieve the catalog of available Neural TTS voices.

    Args:
        region: Azure region override.
        subscription_key: Azure subscription key override.
        locale_filter: Optional locale to filter results (e.g., 'en-US').

    Returns:
        List of VoiceInfo objects representing available Azure voices.
    """
    region = region or AZURE_SPEECH_REGION
    key = subscription_key or AZURE_SPEECH_KEY

    if not validate_azure_credentials(region, key):
        return []

    voices_endpoint = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/voices/list"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "User-Agent": "AzureTTSServiceIntegration/1.0",
    }

    try:
        response = requests.get(voices_endpoint, headers=headers, timeout=30)
        response.raise_for_status()

        voices = parse_azure_voice_list_response(response.text)

        if locale_filter:
            normalized = normalize_locale(locale_filter)
            voices = [v for v in voices if v.locale == normalized]

        return voices

    except requests.exceptions.RequestException:
        return []


def select_voice_for_locale(
    locale: str,
    region: Optional[str] = None,
    subscription_key: Optional[str] = None,
    preferred_gender: str = "",
) -> Optional[VoiceInfo]:
    """
    Select a voice matching the target locale from Azure Cognitive Services.

    Retrieves the voice list from Azure and returns the first matching
    Neural voice for the specified locale, optionally filtered by gender.

    Args:
        locale: Target locale (e.g., 'en-US', 'fr-FR').
        region: Azure region override.
        subscription_key: Azure subscription key override.
        preferred_gender: Optional gender filter ('Male' or 'Female').

    Returns:
        VoiceInfo for the selected voice, or None if no match.
    """
    normalized = normalize_locale(locale)
    voices = list_voices(
        region=region,
        subscription_key=subscription_key,
        locale_filter=normalized,
    )

    if preferred_gender:
        filtered = [v for v in voices if v.gender == preferred_gender]
        return filtered[0] if filtered else None

    return voices[0] if voices else None


def get_voice_for_locale_fallback(
    locale: str,
    preferred_gender: str = "",
) -> Optional[str]:
    """
    Select a voice for a locale using the local fallback catalog.

    Uses the SUPPORTED_LOCALES mapping from speech_client.py to
    find an Azure Neural voice without making an API call.

    Args:
        locale: Target locale string.
        preferred_gender: Optional gender hint ('Male' or 'Female').

    Returns:
        Voice name string or None.
    """
    normalized = normalize_locale(locale)
    voices = SUPPORTED_LOCALES.get(normalized, [])
    if not voices:
        return None

    if preferred_gender:
        for v in voices:
            if preferred_gender.lower() == "female" and ("Aria" in v or "Jenny" in v or "Nanami" in v or "Xiaoxiao" in v or "Elvira" in v or "Denise" in v or "Sonia" in v or "Francisca" in v or "Katja" in v):
                return v
            elif preferred_gender.lower() == "male" and ("Guy" in v or "Davis" in v or "Keita" in v or "Yunxi" in v or "Alvaro" in v or "Henri" in v or "Ryan" in v or "Antonio" in v or "Conrad" in v):
                return v

    return voices[0] if voices else None


def list_supported_locales() -> dict:
    """
    Return the locally configured supported locales and voices.

    Returns:
        Dictionary mapping locale strings to lists of Azure voice names.
    """
    return dict(SUPPORTED_LOCALES)
