from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


def moderation_summary(decisions: List[str]) -> str:
    client = OpenAI()
    prompt = "Summarize these moderation decisions for an operations lead:\n" + "\n".join(decisions)
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    return resp.choices[0].message.content or ""
