from __future__ import annotations

import os
from typing import Any

import requests

from speech_models import normalize_audio_format, normalize_locale


ELEVENLABS_BASE_URL = "https://api.elevenlabs.io"
GOOGLE_TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"
OPENAI_BASE_URL = "https://api.openai.com/v1"


def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def build_elevenlabs_headers() -> dict[str, str]:
    return {
        "xi-api-key": get_env("ELEVENLABS_API_KEY"),
        "Accept": "audio/mpeg",
    }


def build_json_headers(provider: str = "openai") -> dict[str, str]:
    if provider == "openai":
        return {
            "Authorization": f"Bearer {get_env('OPENAI_API_KEY')}",
            "Content-Type": "application/json",
        }
    raise ValueError(f"Unsupported provider: {provider}")


def build_google_params() -> dict[str, str]:
    return {"key": get_env("GOOGLE_CLOUD_API_KEY")}


def build_tts_payload(
    text: str,
    voice_id: str,
    audio_format: str = "mp3",
    speaking_rate: float | None = None,
    pitch: float | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
    }
    payload["output_format"] = (
        "mp3_44100_128"
        if normalize_audio_format(audio_format) == "mp3"
        else "pcm_44100"
    )
    if speaking_rate is not None or pitch is not None:
        payload["voice_settings"] = {}
        if speaking_rate is not None:
            stability = max(0.0, min(1.0, 1.0 - abs(speaking_rate - 1.0) * 0.5))
            payload["voice_settings"]["stability"] = stability
        if pitch is not None:
            payload["voice_settings"]["similarity_boost"] = max(
                0.0, min(1.0, 0.75 + (pitch * 0.05))
            )
    return payload


def normalize_voice_record(record: dict[str, Any]) -> dict[str, Any]:
    labels = record.get("labels") or {}
    preview_locale = normalize_locale(labels.get("accent") or labels.get("language"))
    return {
        "id": record.get("voice_id"),
        "name": record.get("name"),
        "locale": preview_locale or "und",
        "gender": labels.get("gender"),
        "sample_rate_hz": 44100,
    }


def request_json(method: str, url: str, **kwargs: Any) -> dict[str, Any]:
    response = requests.request(method=method, url=url, timeout=60, **kwargs)
    response.raise_for_status()
    return response.json()


def request_bytes(method: str, url: str, **kwargs: Any) -> requests.Response:
    response = requests.request(method=method, url=url, timeout=120, **kwargs)
    response.raise_for_status()
    return response
