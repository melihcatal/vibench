from __future__ import annotations

from google.cloud import texttospeech

from speech_client import get_client, load_speech_config
from speech_models import normalize_ssml


def synthesize_ssml(ssml: str, language_code: str | None = None, voice_name: str | None = None, speaking_rate: float = 1.0, pitch: float = 0.0) -> bytes:
    client = get_client()
    config = load_speech_config()
    input_ssml = texttospeech.SynthesisInput(ssml=normalize_ssml(ssml))
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code or config.default_language_code,
        name=voice_name or config.default_voice_name or "",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=config.audio_encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    response = client.synthesize_speech(input=input_ssml, voice=voice, audio_config=audio_config)
    return response.audio_content
