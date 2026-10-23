from __future__ import annotations

import io
import os

from elevenlabs.client import ElevenLabs


ELEVENLABS_MODEL = "eleven_multilingual_v2"
DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"


def reviewer_brief_audio(brief_text: str, voice_id: str = DEFAULT_VOICE_ID) -> dict:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=ELEVENLABS_MODEL,
        text=brief_text,
        output_format="mp3_44100_128",
    )
    buffer = io.BytesIO()
    for chunk in audio_stream:
        if chunk:
            buffer.write(chunk)
    audio_bytes = buffer.getvalue()
    return {
        "provider": "ElevenLabs Text to Speech",
        "model": ELEVENLABS_MODEL,
        "voice_id": voice_id,
        "audio_bytes": audio_bytes,
        "content_type": "audio/mpeg",
    }
