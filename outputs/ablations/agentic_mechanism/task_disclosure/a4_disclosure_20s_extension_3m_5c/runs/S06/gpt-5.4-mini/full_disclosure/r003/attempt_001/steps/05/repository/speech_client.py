import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_TTS_API_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


@dataclass
class SpeechClientConfig:
    api_key: str
    model: str = OPENAI_TTS_MODEL
    base_url: str = OPENAI_TTS_API_URL
    default_voice: str = "alloy"
    default_format: str = "mp3"
    timeout: int = 120


def load_config(api_key: Optional[str] = None, model: str = OPENAI_TTS_MODEL, base_url: str = OPENAI_TTS_API_URL, default_voice: str = "alloy", default_format: str = "mp3", timeout: int = 120) -> SpeechClientConfig:
    resolved_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not resolved_api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return SpeechClientConfig(api_key=resolved_api_key, model=model, base_url=base_url, default_voice=default_voice, default_format=default_format, timeout=timeout)


def create_session(api_key: Optional[str] = None, model: str = OPENAI_TTS_MODEL, base_url: str = OPENAI_TTS_API_URL, default_voice: str = "alloy", default_format: str = "mp3", timeout: int = 120) -> Dict[str, Any]:
    config = load_config(api_key=api_key, model=model, base_url=base_url, default_voice=default_voice, default_format=default_format, timeout=timeout)
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {config.api_key}", "Content-Type": "application/json"})
    return {"config": config, "session": session}


def build_tts_request(text: str, voice: Optional[str] = None, format: Optional[str] = None, speed: Optional[float] = None, api_key: Optional[str] = None, model: str = OPENAI_TTS_MODEL, base_url: str = OPENAI_TTS_API_URL, default_voice: str = "alloy", default_format: str = "mp3", timeout: int = 120) -> Dict[str, Any]:
    config = load_config(api_key=api_key, model=model, base_url=base_url, default_voice=default_voice, default_format=default_format, timeout=timeout)
    payload: Dict[str, Any] = {"model": config.model, "input": text, "voice": voice or config.default_voice, "format": format or config.default_format}
    if speed is not None:
        payload["speed"] = speed
    return {"config": config, "url": config.base_url, "payload": payload}


def synthesize_bytes(text: str, voice: Optional[str] = None, format: Optional[str] = None, speed: Optional[float] = None, api_key: Optional[str] = None, model: str = OPENAI_TTS_MODEL, base_url: str = OPENAI_TTS_API_URL, default_voice: str = "alloy", default_format: str = "mp3", timeout: int = 120) -> bytes:
    request_data = build_tts_request(text=text, voice=voice, format=format, speed=speed, api_key=api_key, model=model, base_url=base_url, default_voice=default_voice, default_format=default_format, timeout=timeout)
    response = requests.post(request_data["url"], headers={"Authorization": f"Bearer {request_data['config'].api_key}", "Content-Type": "application/json"}, json=request_data["payload"], timeout=request_data["config"].timeout)
    response.raise_for_status()
    return response.content
