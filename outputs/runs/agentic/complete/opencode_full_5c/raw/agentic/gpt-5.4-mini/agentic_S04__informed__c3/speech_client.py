import os
from typing import Optional


def get_api_key() -> str:
    key = os.getenv("ASSEMBLYAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return key


def get_base_url() -> str:
    return os.getenv("ASSEMBLYAI_BASE_URL", "https://api.assemblyai.com/v2").rstrip("/")


def get_headers() -> dict:
    return {
        "authorization": get_api_key(),
        "content-type": "application/json",
    }


def build_audio_url(source: str) -> str:
    if source.startswith("http://") or source.startswith("https://"):
        return source
    return source


def require_webhook_url(webhook_url: Optional[str]) -> str:
    if webhook_url:
        return webhook_url
    value = os.getenv("TRANSCRIPTION_WEBHOOK_URL", "").strip()
    if not value:
        raise RuntimeError(
            "TRANSCRIPTION_WEBHOOK_URL is required for webhook-based jobs"
        )
    return value
