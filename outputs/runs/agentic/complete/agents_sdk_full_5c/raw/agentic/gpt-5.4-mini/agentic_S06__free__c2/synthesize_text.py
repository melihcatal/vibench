from __future__ import annotations

from google.cloud import texttospeech

from speech_client import get_client, load_speech_config
from speech_models import normalize_text, synth_response_from_api


def synthesize_text(text: str, language_code: str | None = None, voice_name: str | None = None) -> bytes:
    client = get_client()
    config = load_speech_config()
    input_text = texttospeech.SynthesisInput(text=normalize_text(text))
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code or config.default_language_code,
        name=voice_name or config.default_voice_name or "",
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=config.audio_encoding)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return synth_response_from_api(response, voice.name or None, config.audio_encoding).audio_content
