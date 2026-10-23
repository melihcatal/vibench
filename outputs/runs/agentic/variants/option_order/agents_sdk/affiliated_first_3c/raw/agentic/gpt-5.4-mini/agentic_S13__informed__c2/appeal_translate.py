from __future__ import annotations

from typing import Optional

from openai import OpenAI


def appeal_translate(text: str, target_language: str = "en") -> str:
    client = OpenAI()
    prompt = f"Translate this moderation appeal into {target_language}:\n{text}"
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    return resp.choices[0].message.content or ""
