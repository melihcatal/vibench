import json
import os
import re
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


@dataclass(frozen=True)
class UnsafeSpan:
    start: int
    end: int
    label: str = "unsafe"


def _merge_spans(spans: Sequence[Tuple[int, int]]) -> List[Tuple[int, int]]:
    ordered = sorted((s, e) for s, e in spans if s < e)
    if not ordered:
        return []
    merged = [ordered[0]]
    for start, end in ordered[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def _mask_text(text: str, spans: Sequence[Tuple[int, int]], replacement: str = "[REDACTED]") -> str:
    merged = _merge_spans(spans)
    if not merged:
        return text
    parts: List[str] = []
    cursor = 0
    for start, end in merged:
        start = max(0, min(start, len(text)))
        end = max(0, min(end, len(text)))
        if start > cursor:
            parts.append(text[cursor:start])
        parts.append(replacement)
        cursor = max(cursor, end)
    if cursor < len(text):
        parts.append(text[cursor:])
    return "".join(parts)


def _heuristic_unsafe_spans(text: str) -> List[Tuple[int, int]]:
    patterns = [
        r"\b(?:sk-|rk-|pk-|ak-)[A-Za-z0-9]{16,}\b",
        r"\b(?:eyJ[A-Za-z0-9_=-]{10,}\.[A-Za-z0-9_=-]{10,}\.[A-Za-z0-9_=-]{10,})\b",
        r"\b(?:\d[ -]*?){13,19}\b",
        r"\b\d{3}-\d{2}-\d{4}\b",
        r"\b(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}\b",
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    ]
    spans: List[Tuple[int, int]] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            spans.append(match.span())
    return _merge_spans(spans)


def _openai_redact_spans(text: str) -> List[Tuple[int, int]]:
    if not OPENAI_API_KEY:
        return _heuristic_unsafe_spans(text)
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": (
                    "Identify unsafe spans in the provided text. Return strict JSON with key spans, "
                    "where each span is an object containing start, end, and label. "
                    "Only include spans that should be redacted."
                ),
            },
            {"role": "user", "content": text},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "unsafe_spans",
                "schema": {
                    "type": "object",
                    "properties": {
                        "spans": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "start": {"type": "integer"},
                                    "end": {"type": "integer"},
                                    "label": {"type": "string"},
                                },
                                "required": ["start", "end", "label"],
                                "additionalProperties": False,
                            },
                        }
                    },
                    "required": ["spans"],
                    "additionalProperties": False,
                },
            },
        },
    }
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    text_out = ""
    if isinstance(data, dict):
        output = data.get("output", [])
        for item in output:
            content = item.get("content", []) if isinstance(item, dict) else []
            for block in content:
                if isinstance(block, dict) and block.get("type") in {"output_text", "text"}:
                    text_out += block.get("text", "")
    if not text_out:
        return _heuristic_unsafe_spans(text)
    try:
        parsed = json.loads(text_out)
        spans = [(int(x["start"]), int(x["end"])) for x in parsed.get("spans", [])]
        return _merge_spans(spans)
    except Exception:
        return _heuristic_unsafe_spans(text)


def redact_unsafe(text: str, replacement: str = "[REDACTED]") -> str:
    spans = _openai_redact_spans(text)
    return _mask_text(text, spans, replacement=replacement)


def flag_unsafe(text: str) -> List[UnsafeSpan]:
    spans = _openai_redact_spans(text)
    return [UnsafeSpan(start=s, end=e) for s, e in spans]


def main() -> None:
    import sys

    data = sys.stdin.read()
    sys.stdout.write(redact_unsafe(data))


if __name__ == "__main__":
    main()
