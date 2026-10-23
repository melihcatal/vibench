from __future__ import annotations

import os

from openai import OpenAI


def summarize_moderation_decisions(
    decisions: list[dict], model: str = "gpt-4o-mini"
) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = {
        "role": "user",
        "content": (
            "Summarize these moderation decisions for an operations reviewer with focus on trends, "
            "highest risk categories, and recommended next actions: "
            f"{decisions}"
        ),
    }
    response = client.chat.completions.create(
        model=model,
        messages=[prompt],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
