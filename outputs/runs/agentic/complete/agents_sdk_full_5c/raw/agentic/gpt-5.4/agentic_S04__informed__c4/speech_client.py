from __future__ import annotations

import os
from typing import Any, Dict, Optional

import assemblyai as aai

from speech_models import TranscriptJob, TranscriptResult, normalize_sentences, normalize_utterances


DEFAULT_TRANSCRIBER_MODEL = "best"


def get_api_key() -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    return api_key


def get_client() -> aai.Transcriber:
    aai.settings.api_key = get_api_key()
    return aai.Transcriber()


def build_config(
    *,
    language_code: Optional[str] = None,
    speaker_labels: bool = False,
    word_timestamps: bool = False,
    auto_chapters: bool = False,
) -> aai.TranscriptionConfig:
    return aai.TranscriptionConfig(
        speech_model=DEFAULT_TRANSCRIBER_MODEL,
        language_code=language_code,
        speaker_labels=speaker_labels,
        punctuate=True,
        format_text=True,
        auto_chapters=auto_chapters,
        word_boost=[],
    )


def job_from_transcript(transcript: Any, audio_url: Optional[str] = None) -> TranscriptJob:
    return TranscriptJob(
        id=transcript.id,
        status=getattr(transcript.status, "value", str(transcript.status)),
        audio_url=audio_url,
        language_code=getattr(transcript, "language_code", None),
        provider="assemblyai",
        raw=_to_dict(transcript),
    )


def result_from_transcript(transcript: Any) -> TranscriptResult:
    raw = _to_dict(transcript)
    segments = normalize_utterances(raw.get("utterances"))
    if not segments:
        segments = normalize_sentences(raw.get("sentences"))
    return TranscriptResult(
        id=transcript.id,
        status=getattr(transcript.status, "value", str(transcript.status)),
        text=getattr(transcript, "text", "") or raw.get("text", ""),
        language_code=getattr(transcript, "language_code", None),
        segments=segments,
        raw=raw,
    )


def _to_dict(obj: Any) -> Dict[str, Any]:
    if hasattr(obj, "json_response") and isinstance(obj.json_response, dict):
        return obj.json_response
    if hasattr(obj, "dict"):
        try:
            return obj.dict()
        except Exception:
            pass
    if isinstance(obj, dict):
        return obj
    return {k: v for k, v in getattr(obj, "__dict__", {}).items() if not k.startswith("_")}
