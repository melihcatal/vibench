"""
select_voice.py - Lists or selects a voice for a target locale using Google Cloud Text-to-Speech.

Uses the google-cloud-texttospeech SDK to enumerate available voices,
filter by language code and gender, and select the optimal voice based
on quality tier (Neural2 > Studio > WaveNet > Standard).
"""

from __future__ import annotations

import os
from typing import List, Optional

from speech_client import SpeechClientHelper
from speech_models import SSMLGenderEnum, VoiceFilter, VoiceInfo


def list_voices(
    language_code: str = "en-US",
    ssml_gender: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> List[VoiceInfo]:
    """
    List available Google Cloud Text-to-Speech voices for a target locale.

    Provider: Google Cloud Text-to-Speech via google-cloud-texttospeech SDK.
    API endpoint: texttospeech.googleapis.com

    Args:
        language_code: BCP-47 language code, e.g. "en-US", "fr-FR", "ja-JP".
        ssml_gender: Optional gender filter - MALE, FEMALE, or NEUTRAL.
        credentials_path: Path to Google service account JSON file.

    Returns:
        List of VoiceInfo objects matching the criteria.

    Raises:
        google.api_core.exceptions.GoogleAPIError: On Google Cloud API failure.
    """
    gender = SSMLGenderEnum(ssml_gender) if ssml_gender else None
    voice_filter = VoiceFilter(
        language_code=language_code,
        ssml_gender=gender,
    )

    client = SpeechClientHelper(credentials_path=credentials_path)
    response = client.list_voices(voice_filter)

    return response.voices


def select_voice(
    language_code: str = "en-US",
    ssml_gender: Optional[str] = None,
    model_preference: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> Optional[VoiceInfo]:
    """
    Select the best available Google Cloud voice for a target locale and gender.

    Prioritizes voices by quality tier:
    - Neural2 (highest quality neural voices)
    - Studio (expressive studio voices)
    - WaveNet (high quality neural)
    - Standard (basic synthetic)

    Provider: Google Cloud Text-to-Speech via google-cloud-texttospeech SDK.
    API endpoint: texttospeech.googleapis.com

    Args:
        language_code: BCP-47 language code, e.g. "en-US", "de-DE".
        ssml_gender: Optional gender preference - MALE, FEMALE, or NEUTRAL.
        model_preference: Optional model type preference (NEURAL2, WAVENET, STANDARD).
        credentials_path: Path to Google service account JSON file.

    Returns:
        VoiceInfo for the selected voice, or None if no voices match.

    Raises:
        google.api_core.exceptions.GoogleAPIError: On Google Cloud API failure.
    """
    gender = SSMLGenderEnum(ssml_gender) if ssml_gender else None
    voice_filter = VoiceFilter(
        language_code=language_code,
        ssml_gender=gender,
        model=model_preference,
    )

    client = SpeechClientHelper(credentials_path=credentials_path)
    selected = client.select_voice(voice_filter)

    if model_preference:
        model_upper = model_preference.upper()
        for voice in client.list_voices(voice_filter).voices:
            for m in voice.supported_models:
                if model_upper in m.upper():
                    return voice

    return selected


def get_voice_details(
    voice_name: str,
    language_code: str = "en-US",
    credentials_path: Optional[str] = None,
) -> Optional[VoiceInfo]:
    """
    Get details for a specific Google Cloud voice by name.

    Args:
        voice_name: Full Google voice name, e.g. "en-US-Wavenet-D".
        language_code: BCP-47 language code for the voice.
        credentials_path: Path to Google service account JSON file.

    Returns:
        VoiceInfo if found, else None.
    """
    voices = list_voices(
        language_code=language_code,
        credentials_path=credentials_path,
    )
    for voice in voices:
        if voice.name == voice_name:
            return voice
    return None


def find_best_voice_for_narration(
    language_code: str = "en-US",
    gender: str = "FEMALE",
    prefer_natural: bool = True,
    credentials_path: Optional[str] = None,
) -> Optional[VoiceInfo]:
    """
    Find the best Google Cloud voice for narration based on naturalness and clarity.

    Args:
        language_code: BCP-47 language code.
        gender: Preferred gender - MALE or FEMALE.
        prefer_natural: If True, prefer Neural2/Studio voices over WaveNet.
        credentials_path: Path to Google service account JSON file.

    Returns:
        VoiceInfo for the best narration voice.
    """
    voice_filter = VoiceFilter(
        language_code=language_code,
        ssml_gender=SSMLGenderEnum(gender),
    )

    client = SpeechClientHelper(credentials_path=credentials_path)
    all_voices = client.list_voices(voice_filter)

    if not all_voices.voices:
        return None

    preferred_models = ["NEURAL2", "STUDIO"] if prefer_natural else ["NEURAL2", "STUDIO", "WAVENET"]

    for model_pref in preferred_models:
        for voice in all_voices.voices:
            for m in voice.supported_models:
                if model_pref in m.upper():
                    return voice

    return all_voices.voices[0]


if __name__ == "__main__":
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    print("Available en-US voices:")
    voices = list_voices(language_code="en-US", credentials_path=creds)
    for v in voices[:5]:
        print(f"  {v.name} - {v.ssml_gender} - models: {v.supported_models[:3]}")

    print("\nBest narration voice:")
    best = find_best_voice_for_narration(
        language_code="en-US",
        gender="FEMALE",
        credentials_path=creds,
    )
    if best:
        print(f"  {best.name} ({best.ssml_gender}) - models: {best.supported_models}")
