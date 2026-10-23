import json
import os
from collections import Counter
from typing import Any, Dict, Iterable, List

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _normalize_decision(item: Dict[str, Any]) -> Dict[str, Any]:
    decision = str(item.get("decision", "")).strip().lower()
    flagged = bool(item.get("flagged", decision in {"block", "reject", "deny"}))
    categories = item.get("categories", [])
    if not isinstance(categories, list):
        categories = []
    return {
        "decision": "block" if flagged else "allow",
        "flagged": flagged,
        "categories": [str(category) for category in categories],
    }


def summarize_moderation(decisions: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    normalized = [_normalize_decision(item) for item in decisions]
    total = len(normalized)
    blocked = sum(1 for item in normalized if item["flagged"])
    allowed = total - blocked
    category_counts: Counter[str] = Counter()
    for item in normalized:
        category_counts.update(item["categories"])

    resp = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize moderation decisions into strict JSON with keys: total (integer), blocked (integer), allowed (integer), top_categories (array of objects with category and count), summary (string). Keep it concise.",
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "total": total,
                        "blocked": blocked,
                        "allowed": allowed,
                        "category_counts": category_counts.most_common(),
                        "decisions": normalized,
                    }
                ),
            },
        ],
        response_format={"type": "json_object"},
    )

    payload = resp.output_text
    try:
        return json.loads(payload)
    except Exception:
        return {
            "total": total,
            "blocked": blocked,
            "allowed": allowed,
            "top_categories": [{"category": name, "count": count} for name, count in category_counts.most_common(5)],
            "summary": payload,
        }
