from __future__ import annotations

import io
import os

from google.cloud import texttospeech


GOOGLE_TTS_VOICE = "en-US-Chirp3-HD-Achernar"


def generate_localized_audio_preview(
    text: str, language_code: str, speaking_rate: float = 1.0
) -> bytes:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=GOOGLE_TTS_VOICE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
    )
    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config,
        }
    )
    buffer = io.BytesIO()
    buffer.write(response.audio_content)
    return buffer.getvalue()
