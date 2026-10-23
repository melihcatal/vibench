import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def build_onboarding_context() -> Dict[str, Any]:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "account_id": _get_env("ONBOARDING_ACCOUNT_ID", "unknown"),
        "customer_name": _get_env("ONBOARDING_CUSTOMER_NAME", "unknown"),
        "plan": _get_env("ONBOARDING_PLAN", "unknown"),
        "stage": _get_env("ONBOARDING_STAGE", "unknown"),
        "blocked": _get_env("ONBOARDING_BLOCKED", "false"),
        "owner": _get_env("ONBOARDING_OWNER", "support"),
        "notes": _get_env("ONBOARDING_NOTES", ""),
    }


def summarize_onboarding_state() -> str:
    api_key = _get_env("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    context = build_onboarding_context()
    prompt = (
        "Summarize the onboarding state for support in 3-5 concise bullets. "
        "Highlight current stage, blockers, ownership, and next action. "
        f"Context: {context}"
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You summarize onboarding status for support teams."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    print(summarize_onboarding_state())
