from __future__ import annotations

import os

from elevenlabs import ElevenLabs

from translation_models import AudioPreviewResult


ELEVENLABS_PROVIDER = "ElevenLabs"
ELEVEN_MULTILINGUAL_VOICE = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
ELEVEN_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


def generate_localized_audio_preview(text: str) -> AudioPreviewResult:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=ELEVEN_MULTILINGUAL_VOICE,
        model_id=ELEVEN_MODEL_ID,
        text=text,
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio)
    return AudioPreviewResult(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        provider=ELEVENLABS_PROVIDER,
        voice=ELEVEN_MULTILINGUAL_VOICE,
        raw_response={"model_id": ELEVEN_MODEL_ID},
    )
