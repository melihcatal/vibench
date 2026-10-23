from __future__ import annotations

from typing import Any

from openai import OpenAI


MODEL = "gpt-4.1-mini"


def moderation_summary(decisions: list[dict[str, Any]]) -> dict[str, Any]:
    client = OpenAI()
    prompt = {
        "role": "user",
        "content": f"Summarize these moderation decisions for an operations reviewer in concise prose: {decisions}",
    }
    response = client.chat.completions.create(
        model=MODEL, messages=[prompt], temperature=0
    )
    text = response.choices[0].message.content or ""
    return {"provider": "openai", "model": MODEL, "summary": text}
