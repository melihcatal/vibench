from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import get_identity_config, make_headers

ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"


def onboarding_summary(onboarding_state: str) -> str:
    cfg = get_identity_config()
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            **make_headers(cfg),
            "x-api-key": cfg.client_secret,
            "anthropic-version": "2023-06-01",
        },
        json={
            "model": ANTHROPIC_MODEL,
            "max_tokens": 300,
            "messages": [
                {"role": "user", "content": f"Summarize this onboarding state for support in one concise paragraph:\n{onboarding_state}"}
            ],
        },
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    data: Dict[str, Any] = resp.json() if resp.content else {}
    content = data.get("content") or []
    if content and isinstance(content, list):
        first = content[0] or {}
        return first.get("text") or onboarding_state
    return onboarding_state
