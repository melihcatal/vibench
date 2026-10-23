from __future__ import annotations

import os
from typing import Optional

from google.cloud import texttospeech

from speech_client import audio_encoding_value, build_client, gender_value, SpeechClientConfig
from speech_models import build_ssml_input


def synthesize_ssml(ssml: str, language_code: Optional[str] = None, voice_name: Optional[str] = None, speaking_rate: float = 1.0, pitch: float = 0.0) -> bytes:
    config = SpeechClientConfig.from_env()
    client = build_client()
    input_ssml = build_ssml_input(ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code or config.language_code,
        name=voice_name or config.voice_name,
        ssml_gender=gender_value(config.ssml_gender),
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding_value(config.audio_encoding),
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    response = client.synthesize_speech(input=input_ssml, voice=voice, audio_config=audio_config)
    return response.audio_content


if __name__ == "__main__":
    print(len(synthesize_ssml(os.getenv("TTS_SSML", "<speak>Hello <break time='200ms'/> world.</speak>"))))
