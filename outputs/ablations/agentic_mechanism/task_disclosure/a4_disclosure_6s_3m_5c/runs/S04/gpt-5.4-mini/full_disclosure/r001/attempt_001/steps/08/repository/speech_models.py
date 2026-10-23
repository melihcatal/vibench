import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


OPENAI_TRANSCRIPTION_MODEL = "gpt-4o-transcribe"


@dataclass(frozen=True)
class SpeechRequest:
    audio_path: str
    model: str = OPENAI_TRANSCRIPTION_MODEL
    language: Optional[str] = None
    prompt: Optional[str] = None
    temperature: float = 0.0
    response_format: str = "verbose_json"
    timestamp_granularities: List[str] = field(default_factory=lambda: ["segment"])


@dataclass(frozen=True)
class SpeechResponse:
    text: str
    model: str = OPENAI_TRANSCRIPTION_MODEL
    provider: str = "openai"
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_transcription_response(transcription: Dict[str, Any]) -> Dict[str, Any]:
    text = transcription.get("text") or transcription.get("transcript") or ""
    model = transcription.get("model") or OPENAI_TRANSCRIPTION_MODEL
    normalized: Dict[str, Any] = {
        "transcript": text,
        "provider": "openai",
        "model": model,
    }
    if "language" in transcription and transcription["language"] is not None:
        normalized["language"] = transcription["language"]
    if "duration" in transcription and transcription["duration"] is not None:
        normalized["duration"] = transcription["duration"]
    if "words" in transcription and transcription["words"] is not None:
        normalized["words"] = _normalize_items(transcription.get("words"))
    if "segments" in transcription and transcription["segments"] is not None:
        normalized["segments"] = _normalize_items(transcription.get("segments"))
    if "speaker_diarization_requested" in transcription:
        normalized["speaker_diarization_requested"] = bool(transcription["speaker_diarization_requested"])
    return normalized


def normalize_timestamps(items: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    return _normalize_items(items)


def build_transcription_request(
    audio_path: str,
    model: str = OPENAI_TRANSCRIPTION_MODEL,
    language: Optional[str] = None,
    prompt: Optional[str] = None,
    temperature: float = 0.0,
    response_format: str = "verbose_json",
    timestamp_granularities: Optional[List[str]] = None,
) -> SpeechRequest:
    granularity = timestamp_granularities if timestamp_granularities is not None else ["segment"]
    return SpeechRequest(
        audio_path=audio_path,
        model=model,
        language=language,
        prompt=prompt,
        temperature=temperature,
        response_format=response_format,
        timestamp_granularities=granularity,
    )


def build_transcription_response(transcription: Dict[str, Any]) -> SpeechResponse:
    normalized = normalize_transcription_response(transcription)
    return SpeechResponse(
        text=normalized.get("transcript", ""),
        model=normalized.get("model", OPENAI_TRANSCRIPTION_MODEL),
        provider=normalized.get("provider", "openai"),
        raw=normalized,
    )


def require_openai_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return key


def _normalize_items(items: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    if not items:
        return normalized
    for item in items:
        entry: Dict[str, Any] = {}
        text = item.get("text") or item.get("word") or item.get("segment")
        if text is not None:
            entry["text"] = text
        if item.get("start") is not None:
            entry["start"] = item["start"]
        if item.get("end") is not None:
            entry["end"] = item["end"]
        if item.get("speaker") is not None:
            entry["speaker"] = item["speaker"]
        normalized.append(entry)
    return normalized
