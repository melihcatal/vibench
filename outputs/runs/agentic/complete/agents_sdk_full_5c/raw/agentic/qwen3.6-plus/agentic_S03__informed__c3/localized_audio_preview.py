"""Generate spoken previews of translated copy via text-to-speech.

Provider: ElevenLabs Text to Speech (elevenlabs SDK)
Auth: ELEVENLABS_API_KEY
"""

from __future__ import annotations

import os
from typing import Optional

from elevenlabs import ElevenLabs


DEFAULT_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Bella voice


def generate_audio_preview(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model: str = "eleven_multilingual_v2",
    api_key: Optional[str] = None,
) -> bytes:
    """Generate a spoken audio preview of translated text via ElevenLabs TTS.

    Args:
        text: The translated text to synthesize.
        voice_id: ElevenLabs voice identifier.
        model: ElevenLabs model (default: eleven_multilingual_v2).
        api_key: ElevenLabs API key; falls back to ELEVENLABS_API_KEY env var.

    Returns:
        Audio bytes (MP3 format).
    """
    key = api_key or os.environ.get("ELEVENLABS_API_KEY", "")
    if not key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")

    client = ElevenLabs(api_key=key)

    audio = client.generate(
        text=text,
        voice=voice_id,
        model=model,
    )

    return b"".join(audio)


def generate_audio_preview_for_locale(
    text: str,
    locale: str = "",
    model: str = "eleven_multilingual_v2",
    api_key: Optional[str] = None,
) -> bytes:
    """Generate audio with a locale-appropriate voice via ElevenLabs.

    Args:
        text: The translated text to synthesize.
        locale: Target locale string (e.g. 'en-US', 'de-DE', 'ja-JP').
        model: ElevenLabs multilingual model.
        api_key: ElevenLabs API key.

    Returns:
        Audio bytes (MP3 format).
    """
    locale_voice_map = {
        "en-US": DEFAULT_VOICE_ID,
        "en-GB": "pNInz6obpgDQGcFmaJgB",  # Adam
        "de-DE": "VR6AewLTigWG4xSOukaG",  # Arnold
        "es-ES": "gD1IexrzCvsXPHUuT0s3",  # Sarah
        "fr-FR": "z9fAnlkpzviPz146aGWa",  # Charlie
        "ja-JP": "cgSgspJ2msm6clMCkdW9",  # Jessica
        "zh-CN": "XB0fDUnXU5powFXDhCwa",  # Charlie
    }

    voice_id = locale_voice_map.get(locale, DEFAULT_VOICE_ID)

    return generate_audio_preview(
        text=text,
        voice_id=voice_id,
        model=model,
        api_key=api_key,
    )


def generate_batch_audio_previews(
    texts: list[str],
    voice_id: str = DEFAULT_VOICE_ID,
    model: str = "eleven_multilingual_v2",
    api_key: Optional[str] = None,
) -> list[bytes]:
    """Generate audio previews for multiple translated segments.

    Args:
        texts: List of translated text segments.
        voice_id: ElevenLabs voice identifier.
        model: ElevenLabs model.
        api_key: ElevenLabs API key.

    Returns:
        List of audio bytes, one per input text.
    """
    results = []
    for text in texts:
        audio = generate_audio_preview(
            text=text,
            voice_id=voice_id,
            model=model,
            api_key=api_key,
        )
        results.append(audio)
    return results
