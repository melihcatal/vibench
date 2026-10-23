from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class TranscriptionRequest:
    audio_path: str
    language: Optional[str] = None
    model: Optional[str] = None
    webhook_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def _file_payload(audio_path: str) -> Dict[str, Any]:
    return {"buffer": Path(audio_path).read_bytes(), "mimetype": "audio/wav"}


def build_transcription_payload(audio_path: str, *, language: Optional[str], model: Optional[str], webhook_url: Optional[str], metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"file": _file_payload(audio_path), "model": model or "nova-2"}
    if language:
        payload["language"] = language
    if webhook_url:
        payload["callback"] = webhook_url
    if metadata:
        payload["metadata"] = metadata
    return payload


def build_diarization_payload(audio_path: str, *, speakers: int, language: Optional[str], model: Optional[str]) -> Dict[str, Any]:
    payload = build_transcription_payload(audio_path, language=language, model=model, webhook_url=None, metadata=None)
    payload["diarize"] = True
    payload["diarize_speaker_count"] = speakers
    return payload


def build_timestamped_payload(audio_path: str, *, words: bool, language: Optional[str], model: Optional[str]) -> Dict[str, Any]:
    payload = build_transcription_payload(audio_path, language=language, model=model, webhook_url=None, metadata=None)
    payload["timestamps"] = True
    payload["words"] = words
    return payload


def normalize_transcript_response(result: Dict[str, Any]) -> Dict[str, Any]:
    return result


def normalize_timestamped_output(result: Dict[str, Any]) -> Dict[str, Any]:
    return result
