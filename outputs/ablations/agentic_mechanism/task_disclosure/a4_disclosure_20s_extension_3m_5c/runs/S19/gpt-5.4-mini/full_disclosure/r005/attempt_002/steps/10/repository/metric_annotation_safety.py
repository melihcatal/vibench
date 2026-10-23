import os
import json
import urllib.request
import urllib.error
from typing import Any, Dict, Optional


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _extract_text(payload: Dict[str, Any]) -> str:
    for key in ("text", "annotation", "label", "content", "value"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    raise ValueError("Missing text to evaluate")


def _call_openai_moderation(text: str, api_key: str) -> Dict[str, Any]:
    body = json.dumps({"model": OPENAI_MODERATION_MODEL, "input": text}).encode("utf-8")
    req = urllib.request.Request(
        OPENAI_MODERATION_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def check_metric_annotation_safety(payload: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    text = _extract_text(payload)
    result = _call_openai_moderation(text, api_key)
    output = result.get("results", [{}])[0]
    categories = output.get("categories", {}) if isinstance(output, dict) else {}
    category_scores = output.get("category_scores", {}) if isinstance(output, dict) else {}
    flagged = bool(output.get("flagged", False)) if isinstance(output, dict) else False
    return {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "text": text,
    }


def main() -> None:
    import sys

    data = sys.stdin.read().strip()
    payload = json.loads(data) if data else {}
    print(json.dumps(check_metric_annotation_safety(payload), ensure_ascii=False))


if __name__ == "__main__":
    main()
