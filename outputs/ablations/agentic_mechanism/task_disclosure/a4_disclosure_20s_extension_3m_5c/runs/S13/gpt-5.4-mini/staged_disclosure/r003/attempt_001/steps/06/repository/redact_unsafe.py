import os
import re
from typing import Any, Dict, List, Tuple

import requests

OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_text(text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    result = payload["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))
    unsafe_categories: List[str] = [name for name, value in categories.items() if value]
    return {
        "flagged": flagged,
        "unsafe_categories": unsafe_categories,
        "category_scores": category_scores,
        "raw": result,
    }


def _find_spans(text: str) -> List[Tuple[int, int, str]]:
    spans: List[Tuple[int, int, str]] = []
    patterns = [
        (r'\b(?:\d[ -]*?){13,19}\b', "credit_card"),
        (r'\b\d{3}-\d{2}-\d{4}\b', "ssn"),
        (r'\b(?:\d{1,3}\.){3}\d{1,3}\b', "ip_address"),
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', "email"),
        (r'\bsk-[A-Za-z0-9]{16,}\b', "api_key"),
    ]
    for pattern, label in patterns:
        for match in re.finditer(pattern, text):
            spans.append((match.start(), match.end(), label))
    spans.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    merged: List[Tuple[int, int, str]] = []
    for start, end, label in spans:
        if merged and start <= merged[-1][1]:
            prev_start, prev_end, prev_label = merged[-1]
            merged[-1] = (prev_start, max(prev_end, end), prev_label + "," + label)
        else:
            merged.append((start, end, label))
    return merged


def redact_unsafe(text: str, replace_with: str = "[REDACTED]") -> Dict[str, Any]:
    moderation = moderate_text(text)
    spans = _find_spans(text)
    redacted = []
    cursor = 0
    for start, end, label in spans:
        redacted.append(text[cursor:start])
        redacted.append(replace_with)
        cursor = end
    redacted.append(text[cursor:])
    return {
        "text": "".join(redacted),
        "flagged": moderation["flagged"],
        "unsafe_categories": moderation["unsafe_categories"],
        "category_scores": moderation["category_scores"],
        "spans": [{"start": s, "end": e, "label": label} for s, e, label in spans],
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: redact_unsafe.py TEXT")
    print(redact_unsafe(sys.argv[1]))
