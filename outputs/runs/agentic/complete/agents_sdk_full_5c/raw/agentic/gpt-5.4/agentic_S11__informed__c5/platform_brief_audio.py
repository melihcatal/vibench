from __future__ import annotations

import os

from elevenlabs import ElevenLabs

DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


def platform_brief_audio(text: str, voice_id: str = DEFAULT_VOICE_ID, model_id: str = DEFAULT_MODEL_ID) -> bytes:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
        text=text,
    )
    return b"".join(audio)
