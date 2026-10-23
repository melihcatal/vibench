from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_ENV_VAR = "OPENAI_API_KEY"
OPENAI_MODEL = "omni-moderation-latest"


@dataclass
class UnsafeSpan:
    start: int
    end: int
    category: str
    score: float


def _call_openai_moderation(text: str) -> Dict[str, Any]:
    api_key = os.getenv(OPENAI_ENV_VAR)
    if not api_key:
        raise RuntimeError(f"Missing {OPENAI_ENV_VAR}")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _extract_unsafe_spans(text: str, moderation: Dict[str, Any]) -> List[UnsafeSpan]:
    results = moderation.get("results") or []
    if not results:
        return []

    result = results[0]
    categories = result.get("categories") or {}
    scores = result.get("category_scores") or {}
    spans: List[UnsafeSpan] = []

    for category, flagged in categories.items():
        if flagged:
            spans.append(
                UnsafeSpan(
                    start=0,
                    end=len(text),
                    category=category,
                    score=float(scores.get(category, 0.0)),
                )
            )
    return spans


def _apply_redaction(text: str, spans: List[UnsafeSpan], redaction_token: str = "[REDACTED]") -> str:
    if not spans:
        return text

    ordered = sorted(spans, key=lambda s: (s.start, s.end))
    pieces: List[str] = []
    cursor = 0

    for span in ordered:
        start = max(0, min(len(text), span.start))
        end = max(start, min(len(text), span.end))
        if start > cursor:
            pieces.append(text[cursor:start])
        if end > cursor:
            pieces.append(redaction_token)
            cursor = end

    if cursor < len(text):
        pieces.append(text[cursor:])

    return "".join(pieces)


def redact_unsafe(text: str, redact: bool = True) -> Dict[str, Any]:
    moderation = _call_openai_moderation(text)
    spans = _extract_unsafe_spans(text, moderation)
    return {
        "unsafe": bool(spans),
        "spans": [span.__dict__ for span in spans],
        "text": _apply_redaction(text, spans) if redact else text,
        "raw_moderation": moderation,
    }


def main() -> None:
    import sys

    input_text = sys.stdin.read()
    result = redact_unsafe(input_text, redact=True)
    sys.stdout.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
