from __future__ import annotations

from google.cloud import texttospeech

from speech_client import get_config, get_tts_client
from speech_models import normalize_text


def synthesize_ssml(ssml: str, voice_name: str | None = None, speaking_rate: float = 1.0, pitch: float = 0.0) -> bytes:
    config = get_config()
    client = get_tts_client()
    synthesis_input = texttospeech.SynthesisInput(ssml=normalize_text(ssml))
    voice = texttospeech.VoiceSelectionParams(
        language_code=config.language_code,
        name=voice_name or config.voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, config.audio_encoding),
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    return response.audio_content
