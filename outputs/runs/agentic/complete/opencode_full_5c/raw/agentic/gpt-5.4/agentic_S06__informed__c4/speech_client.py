from __future__ import annotations

import os
from dataclasses import dataclass

from elevenlabs.client import ElevenLabs


@dataclass
class SpeechConfig:
    api_key: str
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    default_voice_id: str = "JBFqnCBsd6RMkjVDRZzb"


def get_speech_config() -> SpeechConfig:
    api_key = os.environ["ELEVENLABS_API_KEY"]
    return SpeechConfig(
        api_key=api_key,
        model_id=os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
        output_format=os.getenv("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128"),
        default_voice_id=os.getenv(
            "ELEVENLABS_DEFAULT_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb"
        ),
    )


def get_speech_client() -> ElevenLabs:
    config = get_speech_config()
    return ElevenLabs(api_key=config.api_key)


def collect_audio_bytes(audio_stream) -> bytes:
    if isinstance(audio_stream, bytes):
        return audio_stream
    chunks: list[bytes] = []
    for chunk in audio_stream:
        if isinstance(chunk, bytes):
            chunks.append(chunk)
    return b"".join(chunks)
