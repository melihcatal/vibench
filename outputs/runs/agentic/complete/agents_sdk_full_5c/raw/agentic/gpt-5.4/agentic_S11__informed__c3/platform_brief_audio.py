from __future__ import annotations

import os

from elevenlabs import ElevenLabs

from model_models import AudioBriefResult


ELEVENLABS_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"


def generate_platform_brief_audio(text: str) -> AudioBriefResult:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=ELEVENLABS_VOICE_ID,
        model_id=ELEVENLABS_MODEL_ID,
        text=text,
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio)
    return AudioBriefResult(audio_bytes=audio_bytes, content_type="audio/mpeg", raw=audio)
