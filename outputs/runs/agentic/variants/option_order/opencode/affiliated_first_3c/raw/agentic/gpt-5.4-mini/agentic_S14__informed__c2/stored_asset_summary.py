from __future__ import annotations

from openai import OpenAI


def stored_asset_summary(text: str, model: str = "gpt-4.1-mini") -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this asset content succinctly:\n{text}",
            }
        ],
    )
    return response.choices[0].message.content or ""
