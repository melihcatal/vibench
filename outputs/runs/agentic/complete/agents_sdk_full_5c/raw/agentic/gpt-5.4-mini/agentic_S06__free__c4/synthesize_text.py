from __future__ import annotations

from google.cloud import texttospeech

from speech_client import get_config, get_tts_client
from speech_models import normalize_text


def synthesize_text(text: str) -> bytes:
    config = get_config()
    client = get_tts_client()
    synthesis_input = texttospeech.SynthesisInput(text=normalize_text(text))
    voice = texttospeech.VoiceSelectionParams(
        language_code=config.language_code,
        name=config.voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, config.audio_encoding),
        speaking_rate=config.speaking_rate,
        pitch=config.pitch,
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    return response.audio_content
