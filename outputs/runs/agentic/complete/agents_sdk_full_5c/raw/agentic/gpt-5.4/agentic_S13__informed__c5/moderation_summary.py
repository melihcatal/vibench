from __future__ import annotations

import os
from typing import Iterable, Mapping

from openai import OpenAI


def moderation_summary(decisions: Iterable[Mapping[str, object]]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    formatted = []
    for idx, item in enumerate(decisions, start=1):
        formatted.append(f"{idx}. flagged={item.get('flagged')} max_severity={item.get('max_severity')} categories={item.get('categories')}")
    prompt = "Summarize these moderation outcomes for an internal trust-and-safety reviewer:\n" + "\n".join(formatted)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You summarize moderation decisions concisely and neutrally."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
