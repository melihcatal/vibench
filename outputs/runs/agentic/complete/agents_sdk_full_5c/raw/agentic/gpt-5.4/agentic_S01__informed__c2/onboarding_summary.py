from __future__ import annotations

import os
from typing import Any, Dict, List

from mistralai import Mistral


MODEL_NAME = "mistral-small-latest"


def onboarding_summary(account_state: Dict[str, Any]) -> str:
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    prompt = _build_prompt(account_state)
    response = client.chat.complete(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Summarize onboarding status for a customer support agent in a concise, factual way."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return response.choices[0].message.content


def _build_prompt(account_state: Dict[str, Any]) -> str:
    lines: List[str] = ["Summarize this onboarding state:"]
    for key, value in account_state.items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)
