import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SpeechConfig:
    google_api_key: Optional[str]
    google_project_id: Optional[str]
    google_location: str
    google_model: str
    openai_api_key: Optional[str]
    openai_model: str


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        google_api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        google_project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT"),
        google_location=os.getenv("GOOGLE_CLOUD_LOCATION", "us"),
        google_model=os.getenv("GOOGLE_SPEECH_MODEL", "chirp_2"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
    )


def google_speech_headers(api_key: Optional[str]) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["x-goog-api-key"] = api_key
    return headers


def normalize_uri(uri: str) -> str:
    if uri.startswith("gs://"):
        return uri
    if uri.startswith("http://") or uri.startswith("https://"):
        return uri
    return f"gs://{uri.lstrip('/')}"


def chunk_text(text: str, size: int = 1200) -> list[str]:
    text = " ".join(text.split())
    return [text[i : i + size] for i in range(0, len(text), size)] if text else []


def safe_get(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current
