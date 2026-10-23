from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI


MODEL = "gpt-4o-mini"


def summarize_moderation_decisions(decisions: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = (
        "Summarize the following moderation decisions for internal trust-and-safety review. "
        "Include overall risk, repeated categories, and suggested reviewer priority.\n\n"
        f"Decisions: {decisions}"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You produce concise moderation summaries."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
