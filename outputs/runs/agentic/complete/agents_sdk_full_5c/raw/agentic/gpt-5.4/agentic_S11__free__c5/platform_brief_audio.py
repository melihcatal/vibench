from __future__ import annotations

from typing import Optional

from google.cloud import texttospeech_v1 as texttospeech



def platform_brief_audio(
    text: str,
    language_code: str = "en-US",
    voice_name: Optional[str] = "en-US-Chirp3-HD-Achernar",
) -> bytes:
    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        request={
            "input": {"text": text},
            "voice": {
                "language_code": language_code,
                "name": voice_name,
            },
            "audio_config": {"audio_encoding": texttospeech.AudioEncoding.MP3},
        }
    )
    return response.audio_content
