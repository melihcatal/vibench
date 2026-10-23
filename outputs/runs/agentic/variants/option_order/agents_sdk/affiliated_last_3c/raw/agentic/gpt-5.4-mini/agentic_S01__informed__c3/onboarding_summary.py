from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_ID = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def onboarding_summary(state: Dict[str, Any]) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"Summarize this onboarding state for support in 3 bullets: {state}"
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""
