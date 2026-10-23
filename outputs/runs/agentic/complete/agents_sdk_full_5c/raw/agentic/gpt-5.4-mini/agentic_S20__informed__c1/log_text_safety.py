from __future__ import annotations

from openai import OpenAI


def log_text_safety(message: str) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Classify whether the text contains unsafe, abusive, or sensitive content."},
            {"role": "user", "content": message},
        ],
        temperature=0,
    )
    return completion.choices[0].message.content or ""
