import os
from typing import Optional

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer

from model_client import load_dashscope_config
from model_models import AudioResult


DASHSCOPE_TTS_MODELS = {
    "cosyvoice-v1": {
        "model_id": "cosyvoice-v1",
        "provider": "dashscope",
        "service": "Alibaba Model Studio / DashScope CosyVoice",
        "voices": ["longxiaochun", "longyue", "longchen"],
        "sample_rate": 48000,
    },
    "sambert-zhiwei-v1": {
        "model_id": "sambert-zhiwei-v1",
        "provider": "dashscope",
        "service": "Alibaba Model Studio / DashScope",
        "voices": ["zhiwei"],
        "sample_rate": 48000,
    },
}


def generate_platform_brief_audio(
    text: str,
    model_id: str = "cosyvoice-v1",
    voice: str = "longxiaochun",
    sample_rate: int = 48000,
    format: str = "wav",
) -> AudioResult:
    config = load_dashscope_config()
    if model_id not in DASHSCOPE_TTS_MODELS:
        raise ValueError(
            f"TTS model '{model_id}' not found. "
            f"Available: {list(DASHSCOPE_TTS_MODELS.keys())}"
        )
    model_info = DASHSCOPE_TTS_MODELS[model_id]
    if voice not in model_info["voices"]:
        raise ValueError(
            f"Voice '{voice}' not available for model '{model_id}'. "
            f"Available voices: {model_info['voices']}"
        )
    synthesizer = SpeechSynthesizer(
        model=model_id,
        voice=voice,
        sample_rate=sample_rate,
        format=format,
    )
    audio_data = synthesizer.call(text)
    request_id = getattr(synthesizer, "request_id", "")
    if not request_id and hasattr(synthesizer, "get_request_id"):
        request_id = synthesizer.get_request_id()
    return AudioResult(
        audio_data=audio_data,
        format=format,
        model_id=model_id,
        request_id=request_id,
        duration_ms=None,
    )


def generate_briefing_audio_with_options(
    text: str,
    model_id: str = "cosyvoice-v1",
    voice: str = "longxiaochun",
    sample_rate: int = 48000,
    format: str = "wav",
    volume: int = 50,
    speech_rate: int = 0,
    pitch_rate: int = 0,
) -> AudioResult:
    config = load_dashscope_config()
    if model_id not in DASHSCOPE_TTS_MODELS:
        raise ValueError(
            f"TTS model '{model_id}' not found. "
            f"Available: {list(DASHSCOPE_TTS_MODELS.keys())}"
        )
    synthesizer = SpeechSynthesizer(
        model=model_id,
        voice=voice,
        sample_rate=sample_rate,
        format=format,
    )
    synthesizer.set_volume(volume)
    synthesizer.set_speech_rate(speech_rate)
    synthesizer.set_pitch_rate(pitch_rate)
    audio_data = synthesizer.call(text)
    request_id = getattr(synthesizer, "request_id", "")
    if not request_id and hasattr(synthesizer, "get_request_id"):
        request_id = synthesizer.get_request_id()
    return AudioResult(
        audio_data=audio_data,
        format=format,
        model_id=model_id,
        request_id=request_id,
        duration_ms=None,
    )


def get_tts_model_info(model_id: str) -> dict:
    if model_id not in DASHSCOPE_TTS_MODELS:
        raise ValueError(f"Unknown TTS model: {model_id}")
    return DASHSCOPE_TTS_MODELS[model_id].copy()
