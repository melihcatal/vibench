from __future__ import annotations

import os
from dataclasses import asdict
from typing import Dict, Optional

from elevenlabs.client import ElevenLabs

from speech_models import SSMLRequest, TTSRequest


DEFAULT_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
DEFAULT_OUTPUT_FORMAT = os.getenv("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128")


def get_elevenlabs_client(api_key: Optional[str] = None) -> ElevenLabs:
    resolved_api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
    if not resolved_api_key:
        raise ValueError("Missing ELEVENLABS_API_KEY")
    return ElevenLabs(api_key=resolved_api_key)


def build_tts_payload(request: TTSRequest) -> Dict[str, object]:
    payload: Dict[str, object] = {
        "text": request.text,
        "model_id": request.model_id or DEFAULT_MODEL_ID,
        "output_format": request.output_format or DEFAULT_OUTPUT_FORMAT,
    }
    if request.voice_id:
        payload["voice_id"] = request.voice_id

    voice_settings = {
        "stability": request.stability,
        "similarity_boost": request.similarity_boost,
        "style": request.style,
        "use_speaker_boost": request.use_speaker_boost,
    }
    cleaned_settings = {k: v for k, v in voice_settings.items() if v is not None}
    if cleaned_settings:
        payload["voice_settings"] = cleaned_settings
    return payload


def build_ssml_payload(request: SSMLRequest) -> Dict[str, object]:
    payload = asdict(request)
    payload["model_id"] = request.model_id or DEFAULT_MODEL_ID
    payload["output_format"] = request.output_format or DEFAULT_OUTPUT_FORMAT
    if not payload.get("voice_id"):
        payload["voice_id"] = DEFAULT_VOICE_ID
    return payload


def iter_audio_bytes(audio_stream) -> bytes:
    if isinstance(audio_stream, (bytes, bytearray)):
        return bytes(audio_stream)
    return b"".join(chunk for chunk in audio_stream if chunk)
