"""List or select a voice for a target locale using Google Cloud Text-to-Speech."""

import os
from typing import List, Optional

from google.cloud import texttospeech
from google.cloud.texttospeech_v1.types import ListVoicesResponse, Voice


def list_voices(
    language_code: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> List[Voice]:
    """List available voices from Google Cloud Text-to-Speech.

    Args:
        language_code: Filter voices by BCP-47 language code (e.g. "en-US", "ja-JP").
        credentials_path: Optional path to service account JSON.
            Falls back to GOOGLE_APPLICATION_CREDENTIALS env var.

    Returns:
        List of google.cloud.texttospeech.Voice objects.
    """
    client_kwargs = {}
    if credentials_path:
        client_kwargs["client_options"] = {
            "credentials_file": credentials_path
        }
    elif not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError(
            "Set GOOGLE_APPLICATION_CREDENTIALS or pass credentials_path"
        )

    client = texttospeech.TextToSpeechClient(**client_kwargs)

    request = texttospeech.ListVoicesRequest(language_code=language_code)
    response: ListVoicesResponse = client.list_voices(request=request)

    return list(response.voices)


def select_voice(
    language_code: str,
    preferred_gender: Optional[str] = None,
    preferred_model: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> Voice:
    """Select the best matching voice for a target locale from Google Cloud TTS.

    Args:
        language_code: Required BCP-47 language code (e.g. "en-US").
        preferred_gender: Optional filter: "MALE", "FEMALE", "SSML_VOICE_GENDER_UNSPECIFIED".
        preferred_model: Optional filter for specific model (e.g. "news", "studio").
        credentials_path: Optional path to service account JSON.

    Returns:
        A single Voice object best matching the criteria.

    Raises:
        ValueError: If no matching voice is found.
    """
    voices = list_voices(
        language_code=language_code,
        credentials_path=credentials_path,
    )

    candidates = voices
    if preferred_gender:
        target_gender = getattr(
            texttospeech.SsmlVoiceGender, preferred_gender.upper(), None
        )
        if target_gender:
            candidates = [
                v for v in candidates if v.ssml_gender == target_gender
            ]

    if preferred_model:
        candidates = [
            v for v in candidates
            if any(preferred_model in n.lower() for n in v.name)
        ]

    if not candidates:
        raise ValueError(
            f"No Google Cloud TTS voice found for language_code={language_code}, "
            f"preferred_gender={preferred_gender}, preferred_model={preferred_model}"
        )

    return candidates[0]


def get_voice_name(voice: Voice) -> str:
    """Extract the voice name string from a Google Cloud TTS Voice object."""
    return voice.name
