from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_ID = "gpt-4o-mini"


def onboarding_summary(onboarding_state: Dict[str, Any]) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"Summarize this onboarding state for support in 3 concise bullets:\n{onboarding_state}"
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize account lifecycle states for support teams."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
