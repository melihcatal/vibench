from __future__ import annotations

from openai import OpenAI

MODEL = "gpt-4o-mini"


def moderation_summary(decisions: list[dict]) -> str:
    client = OpenAI()
    prompt = f"Summarize the following moderation decisions succinctly for an operations reviewer: {decisions}"
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You summarize moderation outcomes clearly and neutrally."},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content or ""
