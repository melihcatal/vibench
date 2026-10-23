from __future__ import annotations

from typing import Iterable, Mapping

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def summarize_moderation(decisions: Iterable[Mapping[str, object]]) -> str:
    client = OpenAI()
    prompt = "Summarize the moderation decisions succinctly for an operations team.\n\n"
    prompt += "\n".join(str(item) for item in decisions)
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize moderation outcomes clearly and neutrally."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
