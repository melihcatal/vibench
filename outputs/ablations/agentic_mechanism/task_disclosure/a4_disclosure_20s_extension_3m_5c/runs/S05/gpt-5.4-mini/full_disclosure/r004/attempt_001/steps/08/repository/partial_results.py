import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_TRANSCRIPTION_API = "https://api.openai.com/v1/audio/transcriptions"


@dataclass
class StreamingRecognitionResult:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    raw: Optional[Dict[str, Any]] = None


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "final"}
    return bool(value)


def parse_partial_result(event: Dict[str, Any]) -> StreamingRecognitionResult:
    text = str(event.get("text") or event.get("transcript") or event.get("alternative", {}).get("transcript") or "")
    is_final = _coerce_bool(event.get("is_final", event.get("final", event.get("speech_final", False))))
    confidence = event.get("confidence")
    if confidence is None and isinstance(event.get("alternative"), dict):
        confidence = event["alternative"].get("confidence")
    try:
        confidence = None if confidence is None else float(confidence)
    except (TypeError, ValueError):
        confidence = None
    return StreamingRecognitionResult(text=text, is_final=is_final, confidence=confidence, raw=event)


def handle_partial_and_final(event: Dict[str, Any]) -> Dict[str, Any]:
    result = parse_partial_result(event)
    return {
        "text": result.text,
        "status": "final" if result.is_final else "partial",
        "confidence": result.confidence,
        "raw": result.raw,
    }


def send_to_openai_transcription(audio_bytes: bytes, filename: str = "audio.wav", model: str = "gpt-4o-mini-transcribe") -> Dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    files = {"file": (filename, audio_bytes)}
    data = {"model": model, "response_format": "verbose_json"}
    response = requests.post(
        OPENAI_TRANSCRIPTION_API,
        headers={"Authorization": f"Bearer {api_key}"},
        files=files,
        data=data,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
