from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Mapping

import requests


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_SUMMARY_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


@dataclass(frozen=True)
class ArchiveSummary:
    summary: str
    raw: dict[str, Any]


def _auth_headers() -> dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _normalize_text(result: Any) -> str:
    if isinstance(result, str):
        return result
    if isinstance(result, Mapping):
        text = result.get("text") or result.get("transcript")
        if isinstance(text, str):
            return text
        segments = result.get("segments") or []
        if segments:
            pieces: list[str] = []
            for segment in segments:
                if isinstance(segment, Mapping):
                    piece = segment.get("text") or segment.get("transcript") or segment.get("word")
                    if piece:
                        pieces.append(str(piece))
            return " ".join(pieces).strip()
    return str(result)


def summarize_transcription_result(result: Any, *, model: str = OPENAI_SUMMARY_MODEL, max_tokens: int = 300) -> ArchiveSummary:
    transcript_text = _normalize_text(result)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Summarize transcription results for archival use."},
            {"role": "user", "content": transcript_text},
        ],
        "temperature": 0.2,
        "max_tokens": max_tokens,
    }
    response = requests.post(
        f"{OPENAI_API_BASE}/chat/completions",
        headers=_auth_headers(),
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    summary = data["choices"][0]["message"]["content"].strip()
    return ArchiveSummary(summary=summary, raw=data)
