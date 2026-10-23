from dataclasses import dataclass
import os
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class SpeechConfig:
    assemblyai_api_key: str
    assemblyai_realtime_url: str = "wss://stream.assemblyai.com/v3/realtime"
    assemblyai_base_url: str = "https://api.assemblyai.com"


def load_config() -> SpeechConfig:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY", "")
    return SpeechConfig(assemblyai_api_key=api_key)


def auth_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    key = api_key or load_config().assemblyai_api_key
    return {"authorization": key, "content-type": "application/json"}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("text", "transcript", "content", "summary"):
            if key in value and value[key] is not None:
                return normalize_text(value[key])
    return str(value).strip()


def transcript_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "text": normalize_text(payload.get("text")),
        "is_final": bool(
            payload.get("message_type") == "FinalTranscript" or payload.get("is_final")
        ),
        "confidence": payload.get("confidence"),
        "language": payload.get("language_code") or payload.get("language"),
    }
