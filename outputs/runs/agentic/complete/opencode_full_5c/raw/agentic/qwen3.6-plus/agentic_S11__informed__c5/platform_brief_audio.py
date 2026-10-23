import os
from typing import Optional

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer

from model_client import load_dashscope_api_key
from model_models import AudioResult


TTS_MODEL = "cosyvoice-v1"
DEFAULT_VOICE = "longxiaochun"


def generate_platform_brief_audio(
    text: str,
    model: Optional[str] = None,
    voice: Optional[str] = None,
    sample_rate: int = 48000,
    format_type: str = "wav",
) -> AudioResult:
    load_dashscope_api_key()

    model_id = model or TTS_MODEL
    voice_id = voice or DEFAULT_VOICE

    synthesizer = SpeechSynthesizer(
        model=model_id,
        voice=voice_id,
        format=format_type,
        sample_rate=sample_rate,
    )

    audio_data = synthesizer.call(text)

    if audio_data is None:
        raise RuntimeError(
            f"DashScope CosyVoice TTS returned no audio for model={model_id}, voice={voice_id}"
        )

    return AudioResult(
        text=text,
        audio_data=audio_data,
        audio_format=format_type,
        model=model_id,
        raw_response={"model": model_id, "voice": voice_id, "sample_rate": sample_rate},
    )


def generate_platform_brief_audio_stream(
    text: str,
    model: Optional[str] = None,
    voice: Optional[str] = None,
    sample_rate: int = 48000,
    format_type: str = "wav",
) -> bytes:
    load_dashscope_api_key()

    model_id = model or TTS_MODEL
    voice_id = voice or DEFAULT_VOICE

    synthesizer = SpeechSynthesizer(
        model=model_id,
        voice=voice_id,
        format=format_type,
        sample_rate=sample_rate,
    )

    audio_chunks = []
    for chunk in synthesizer.streaming_call(text):
        if chunk:
            audio_chunks.append(chunk)

    return b"".join(audio_chunks)
