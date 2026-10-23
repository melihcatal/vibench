from __future__ import annotations

import base64

from translation_client import GOOGLE_TTS_VOICE, split_languages
from google.cloud import texttospeech


def localized_audio_preview(text: str, voice_name: str | None = None, audio_encoding: str = "MP3") -> bytes:
    selected_voice = voice_name or GOOGLE_TTS_VOICE
    language_code = "-".join(split_languages(selected_voice))
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=selected_voice)
    encoding = getattr(texttospeech.AudioEncoding, audio_encoding.upper(), texttospeech.AudioEncoding.MP3)
    audio_config = texttospeech.AudioConfig(audio_encoding=encoding)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    if isinstance(response.audio_content, str):
        return base64.b64decode(response.audio_content)
    return bytes(response.audio_content)
