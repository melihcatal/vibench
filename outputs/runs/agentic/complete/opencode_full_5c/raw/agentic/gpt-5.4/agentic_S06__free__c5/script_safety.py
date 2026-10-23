from __future__ import annotations

from speech_client import OPENAI_BASE_URL, build_json_headers, request_json
from speech_models import SafetyResult


def check_script_safety(text: str) -> SafetyResult:
    response = request_json(
        "POST",
        f"{OPENAI_BASE_URL}/moderations",
        headers=build_json_headers("openai"),
        json={"model": "omni-moderation-latest", "input": text},
    )
    result = response["results"][0]
    categories = {
        key: bool(value) for key, value in result.get("categories", {}).items()
    }
    return SafetyResult(
        flagged=bool(result.get("flagged")), categories=categories, provider="openai"
    )
