import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SpeechServiceConfig:
    provider: str
    api_key: Optional[str]
    endpoint: str
    model: str


def load_config(provider: str = "openai") -> SpeechServiceConfig:
    provider = provider.lower()
    if provider == "microsoft":
        return SpeechServiceConfig(
            provider="microsoft",
            api_key=os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://api.openai.com/v1"),
            model=os.getenv("AZURE_OPENAI_AUDIO_MODEL", "whisper-1"),
        )
    return SpeechServiceConfig(
        provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        endpoint=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
        model=os.getenv("OPENAI_AUDIO_MODEL", "whisper-1"),
    )


def client_headers(api_key: Optional[str]) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def normalize_transcript(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = payload.get("text") or payload.get("transcript") or ""
    segments = payload.get("segments") or payload.get("words") or []
    return {"text": text, "segments": segments, "raw": payload}
