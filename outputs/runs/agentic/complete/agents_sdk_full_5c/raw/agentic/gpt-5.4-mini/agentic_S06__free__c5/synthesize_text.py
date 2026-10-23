from __future__ import annotations

from typing import Optional

from speech_client import build_speech_client, default_voice_name
from speech_models import TextToSpeechRequest, normalize_text

try:
    from google.cloud import texttospeech
except Exception:  # pragma: no cover
    texttospeech = None


DEFAULT_LOCALE = "en-US"


def synthesize_text(text: str, voice_name: Optional[str] = None, locale: str = DEFAULT_LOCALE) -> bytes:
    """Synthesize plain text into audio bytes using Google Cloud Text-to-Speech."""
    client = build_speech_client()
    request = TextToSpeechRequest(text=normalize_text(text), locale=locale, voice_name=voice_name or default_voice_name(locale))

    if texttospeech is None:
        raise RuntimeError("google-cloud-texttospeech is required for synthesize_text")

    synthesis_input = texttospeech.SynthesisInput(text=request.text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=request.locale,
        name=request.voice_name,
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config,
    )
    return response.audio_content
