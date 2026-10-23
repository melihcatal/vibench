import os
import json
import urllib.request
import urllib.error
from typing import Optional

from observability_models import LogEntry


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODERATION_MODEL = "text-moderation-latest"


def check_log_text_safety(
    entries: list[LogEntry],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> list[dict]:
    results = []
    for entry in entries:
        text = entry.message
        if not text:
            continue
        moderation_result = _call_openai_moderation(
            text=text, api_key=api_key, model=model
        )
        flagged = moderation_result.get("results", [{}])[0].get("flagged", False)
        categories = moderation_result.get("results", [{}])[0].get("categories", {})
        scores = moderation_result.get("results", [{}])[0].get("category_scores", {})
        results.append(
            {
                "log_id": entry.id,
                "message_preview": text[:200],
                "flagged": flagged,
                "categories": {k: v for k, v in categories.items() if v},
                "scores": {k: round(v, 4) for k, v in scores.items() if v > 0.001},
                "safe": not flagged,
                "model": model,
                "provider": "openai",
            }
        )
    return results


def _call_openai_moderation(
    text: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> dict:
    url = f"{OPENAI_API_BASE}/moderations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key or OPENAI_API_KEY}",
    }
    payload = {
        "input": text,
        "model": model,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_data = resp.read().decode("utf-8")
            return json.loads(resp_data)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(
            f"OpenAI text-moderation-latest API error {e.code}: {e.reason} - {error_body}"
        ) from e
