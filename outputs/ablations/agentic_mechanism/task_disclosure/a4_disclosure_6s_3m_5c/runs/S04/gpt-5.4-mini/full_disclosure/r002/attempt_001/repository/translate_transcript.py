from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os

import requests


OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-4.1-mini"


@dataclass
class TranscriptSegment:
    text: str
    start: Optional[float] = None
    end: Optional[float] = None
    speaker: Optional[str] = None


def _segments_to_prompt(segments: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for segment in segments:
        speaker = segment.get("speaker")
        prefix = f"{speaker}: " if speaker else ""
        text = str(segment.get("text", "")).strip()
        if text:
            lines.append(f"{prefix}{text}")
    return "\n".join(lines)


def translate_transcript(segments: List[Dict[str, Any]], target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    transcript = _segments_to_prompt(segments)
    if not transcript:
        return ""

    system_prompt = (
        "You translate completed transcript segments accurately while preserving meaning, "
        "speaker labels, line breaks, and timestamps if present. Return only the translated text."
    )
    user_prompt = f"Translate the following transcript into {target_language}."
    if source_language:
        user_prompt += f" The source language is {source_language}."
    user_prompt += f"\n\n{transcript}"

    response = requests.post(
        f"{OPENAI_API_BASE}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


__all__ = ["translate_transcript", "TranscriptSegment"]
