import os
import json
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _get_env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip()


def _build_payload(onboarding_state: Dict[str, Any]) -> Dict[str, Any]:
    prompt = (
        "Summarize the onboarding state for a support agent in a concise, actionable format. "
        "Focus on completion status, blockers, risks, missing information, and next steps. "
        f"Onboarding state: {json.dumps(onboarding_state, ensure_ascii=False, sort_keys=True)}"
    )
    return {
        "model": OPENAI_MODEL,
        "input": prompt,
        "temperature": 0.2,
        "max_output_tokens": 300,
    }


def summarize_onboarding_state(onboarding_state: Dict[str, Any], api_key: Optional[str] = None) -> str:
    token = api_key or _get_env("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=_build_payload(onboarding_state),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    output_text = data.get("output_text")
    if output_text:
        return output_text.strip()

    parts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if text:
                parts.append(text)
    return "".join(parts).strip()
