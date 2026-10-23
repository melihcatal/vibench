import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


@dataclass
class AnnotationSafetyResult:
    unsafe: bool
    provider: str
    model: str
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    flagged: List[str]
    raw: Dict[str, Any]


def _extract_text(payload: Dict[str, Any]) -> str:
    for key in ("text", "annotation", "label", "note", "content"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    if "texts" in payload and isinstance(payload["texts"], list):
        return "\n".join(str(item) for item in payload["texts"] if str(item).strip())
    return ""


def check_metric_annotation_safety(annotation: str, api_key: Optional[str] = None, timeout: float = 30.0) -> AnnotationSafetyResult:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODEL, "input": annotation},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    result = (data.get("results") or [{}])[0]
    categories = dict(result.get("categories") or {})
    category_scores = dict(result.get("category_scores") or {})
    flagged = [name for name, value in categories.items() if value]
    return AnnotationSafetyResult(
        unsafe=bool(result.get("flagged")),
        provider="openai",
        model=OPENAI_MODEL,
        categories=categories,
        category_scores=category_scores,
        flagged=flagged,
        raw=data,
    )


def check_metric_annotation_safety_from_payload(payload: Dict[str, Any], api_key: Optional[str] = None, timeout: float = 30.0) -> Dict[str, Any]:
    text = _extract_text(payload)
    result = check_metric_annotation_safety(text, api_key=api_key, timeout=timeout)
    return {
        "unsafe": result.unsafe,
        "provider": result.provider,
        "model": result.model,
        "categories": result.categories,
        "category_scores": result.category_scores,
        "flagged": result.flagged,
        "raw": result.raw,
    }


def main() -> None:
    import sys

    payload = json.loads(sys.stdin.read() or "{}")
    output = check_metric_annotation_safety_from_payload(payload)
    sys.stdout.write(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
