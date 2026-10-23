"""List or select a voice for a target locale using Watson Text to Speech."""

import os
from typing import Optional
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from speech_client import get_watson_tts_credentials, VoiceSelectorConfig
from speech_models import VoiceInfo, VoiceListResponse


def list_vvoices(
    locale_filter: Optional[str] = None,
    apikey: Optional[str] = None,
    url: Optional[str] = None,
) -> VoiceListResponse:
    """List available voices from Watson Text to Speech, optionally filtered by locale.

    Args:
        locale_filter: Locale prefix to filter voices (e.g., 'en', 'fr', 'de').
        apikey: Watson TTS API key (defaults to IBM_TTS_APIKEY env var).
        url: Watson TTS service URL (defaults to IBM_TTS_URL env var).

    Returns:
        VoiceListResponse containing voice metadata.
    """
    if apikey is None or url is None:
        apikey, url = get_watson_tts_credentials()

    authenticator = IAMAuthenticator(apikey)
    service = TextToSpeechV1(authenticator=authenticator)
    service.set_service_url(url)

    response = service.list_voices().get_result()
    voices_data = response.get("voices", [])

    voices = []
    for v in voices_data:
        vi = VoiceInfo(
            voice_id=v.get("name", ""),
            name=v.get("name", ""),
            locale=v.get("language", ""),
            gender=v.get("gender", ""),
            sample_rate=v.get("sample_rate_hz", 22050),
            supported_formats=v.get("supported_features", {}).get("custom_pronunciation", []),
        )
        voices.append(vi)

    result = VoiceListResponse(voices=voices, total_count=len(voices))

    if locale_filter:
        result = result.filter_by_locale(locale_filter)

    return result


def select_voice(
    locale: str,
    gender: Optional[str] = None,
    apikey: Optional[str] = None,
    url: Optional[str] = None,
) -> VoiceInfo:
    """Select the best matching voice for a target locale via Watson TTS.

    Args:
        locale: Target locale code (e.g., 'en-US', 'fr-FR').
        gender: Optional gender preference ('male', 'female', or None).
        apikey: Watson TTS API key.
        url: Watson TTS service URL.

    Returns:
        VoiceInfo for the selected voice.

    Raises:
        ValueError: If no matching voice is found.
    """
    all_voices = list_vvoices(locale_filter=locale, apikey=apikey, url=url)

    if not all_voices.voices:
        raise ValueError(f"No Watson TTS voices found for locale '{locale}'")

    candidates = all_voices.voices

    if gender:
        gendered = [v for v in candidates if v.gender.lower() == gender.lower()]
        if gendered:
            candidates = gendered

    # Prefer voices matching the exact locale first, then any in the language family
    exact_match = [v for v in candidates if v.locale == locale]
    if exact_match:
        return exact_match[0]

    return candidates[0]


if __name__ == "__main__":
    voices = list_vvoices(locale_filter="en")
    print(f"Found {voices.total_count} English voices:")
    for v in voices.voices[:5]:
        print(f"  {v.name} ({v.locale}, {v.gender})")

    selected = select_voice("en-US")
    print(f"\nSelected voice for en-US: {selected.name}")
