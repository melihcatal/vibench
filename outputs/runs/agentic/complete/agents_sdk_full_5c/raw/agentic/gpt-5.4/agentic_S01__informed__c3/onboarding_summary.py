from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

from identity_models import SummaryResult


MODEL_NAME = "gpt-4o-mini"


def onboarding_summary(onboarding_state: Dict[str, Any]) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "Summarize onboarding state for support staff in a concise, factual paragraph with notable blockers and next steps.",
            },
            {"role": "user", "content": str(onboarding_state)},
        ],
        temperature=0.2,
    )
    content = completion.choices[0].message.content or ""
    return SummaryResult(provider="OpenAI", model=MODEL_NAME, summary=content).to_dict()
