from __future__ import annotations

import requests

from identity_client import openai_headers
from identity_models import ModerationResult


def profile_moderation(profile_text: str) -> ModerationResult:
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers=openai_headers(),
        json={"model": "omni-moderation-latest", "input": profile_text},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    result = payload["results"][0]
    categories = [name for name, value in result.get("categories", {}).items() if value]
    return ModerationResult(
        provider="openai",
        approved=not bool(result.get("flagged", False)),
        flagged_categories=categories,
        raw_result=result,
    )
