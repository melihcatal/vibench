from __future__ import annotations

import os

from speech_client import MODERATION_API_URL, get_requests_session


def check_script_safety(text: str, model: str = "omni-moderation-latest") -> dict:
    session = get_requests_session()
    response = session.post(
        MODERATION_API_URL,
        json={"model": model, "input": text},
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()["results"][0]
    return {
        "provider": "openai",
        "model": model,
        "flagged": result["flagged"],
        "categories": result["categories"],
        "category_scores": result.get("category_scores", {}),
    }
