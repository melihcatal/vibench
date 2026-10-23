import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_prompt(onboarding_state: Dict[str, Any]) -> str:
    return (
        "Summarize the onboarding state for support in a concise format. "
        "Highlight account status, completed steps, missing steps, blockers, and recommended next action. "
        f"Onboarding state: {json.dumps(onboarding_state, ensure_ascii=False, sort_keys=True)}"
    )


def summarize_onboarding_state(onboarding_state: Dict[str, Any]) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "input": _build_prompt(onboarding_state),
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    text_parts: List[str] = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text_parts.append(content.get("text", ""))
    if text_parts:
        return "".join(text_parts).strip()
    return json.dumps(data, ensure_ascii=False)


def main() -> None:
    import sys

    raw = sys.stdin.read().strip()
    if not raw:
        raise SystemExit("Provide onboarding state JSON on stdin")
    onboarding_state = json.loads(raw)
    print(summarize_onboarding_state(onboarding_state))


if __name__ == "__main__":
    main()
