from __future__ import annotations

from speech_client import build_speech_client, default_voice_name
from speech_models import SSMLRequest, normalize_ssml

try:
    from google.cloud import texttospeech
except Exception:  # pragma: no cover
    texttospeech = None


DEFAULT_LOCALE = "en-US"


def synthesize_ssml(ssml: str, locale: str = DEFAULT_LOCALE, voice_name: str | None = None) -> bytes:
    """Synthesize SSML with voice and prosody controls using Google Cloud Text-to-Speech."""
    client = build_speech_client()
    request = SSMLRequest(ssml=normalize_ssml(ssml), locale=locale, voice_name=voice_name or default_voice_name(locale))

    if texttospeech is None:
        raise RuntimeError("google-cloud-texttospeech is required for synthesize_ssml")

    synthesis_input = texttospeech.SynthesisInput(ssml=request.ssml)
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
