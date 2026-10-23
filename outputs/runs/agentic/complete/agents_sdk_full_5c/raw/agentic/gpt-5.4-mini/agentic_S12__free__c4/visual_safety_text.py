from __future__ import annotations

from typing import Iterable

from openai import OpenAI


def visual_safety_text(labels: Iterable[str]) -> str:
    client = OpenAI()
    joined = ", ".join(labels)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"Review these image labels for unsafe or policy-sensitive text and provide a brief warning if needed: {joined}",
        max_output_tokens=80,
    )
    return response.output_text.strip()
