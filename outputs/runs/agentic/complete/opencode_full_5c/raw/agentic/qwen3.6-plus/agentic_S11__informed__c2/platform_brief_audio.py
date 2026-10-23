from __future__ import annotations

import os
from typing import Any, Dict, Optional

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer

from model_client import configure_dashscope
from model_models import AudioResult


COSYVOICE_MODEL = "cosyvoice-v1"
DEFAULT_VOICE = "longxiaochun"


def generate_platform_brief_audio(
    text: str,
    model: str = COSYVOICE_MODEL,
    voice: str = DEFAULT_VOICE,
    sample_rate: int = 48000,
    format: str = "wav",
    **kwargs: Any,
) -> AudioResult:
    configure_dashscope()

    synthesizer = SpeechSynthesizer(
        model=model,
        voice=voice,
        format=format,
        sample_rate=sample_rate,
        **kwargs,
    )

    audio_data = synthesizer.call(text)

    return AudioResult(
        audio_data=audio_data,
        model_id=model,
        request_id="",
        raw_response={
            "model": model,
            "voice": voice,
            "format": format,
            "sample_rate": sample_rate,
        },
    )


def generate_brief_audio_to_file(
    text: str,
    output_path: str,
    model: str = COSYVOICE_MODEL,
    voice: str = DEFAULT_VOICE,
    sample_rate: int = 48000,
    format: str = "wav",
    **kwargs: Any,
) -> AudioResult:
    configure_dashscope()

    synthesizer = SpeechSynthesizer(
        model=model,
        voice=voice,
        format=format,
        sample_rate=sample_rate,
        **kwargs,
    )

    audio_data = synthesizer.call(text)

    with open(output_path, "wb") as f:
        f.write(audio_data)

    return AudioResult(
        audio_data=audio_data,
        model_id=model,
        request_id="",
        raw_response={
            "model": model,
            "voice": voice,
            "format": format,
            "sample_rate": sample_rate,
            "output_path": output_path,
        },
    )


def generate_brief_audio_with_options(
    text: str,
    model: str = COSYVOICE_MODEL,
    voice: str = DEFAULT_VOICE,
    sample_rate: int = 48000,
    format: str = "wav",
    volume: int = 50,
    speech_rate: int = 0,
    pitch_rate: int = 0,
    **kwargs: Any,
) -> AudioResult:
    configure_dashscope()

    synthesizer = SpeechSynthesizer(
        model=model,
        voice=voice,
        format=format,
        sample_rate=sample_rate,
        volume=volume,
        speech_rate=speech_rate,
        pitch_rate=pitch_rate,
        **kwargs,
    )

    audio_data = synthesizer.call(text)

    return AudioResult(
        audio_data=audio_data,
        model_id=model,
        request_id="",
        raw_response={
            "model": model,
            "voice": voice,
            "format": format,
            "sample_rate": sample_rate,
            "volume": volume,
            "speech_rate": speech_rate,
            "pitch_rate": pitch_rate,
        },
    )
