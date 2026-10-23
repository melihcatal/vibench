from __future__ import annotations

from typing import Dict

from openai import OpenAI


SAFETY_MODEL = "gpt-4o-mini"


def check_unsafe_copy(text: str) -> Dict[str, str]:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=SAFETY_MODEL,
        messages=[
            {"role": "system", "content": "Assess localized copy for unsafe content and concise remediation."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return {"provider": "openai", "model": SAFETY_MODEL, "result": completion.choices[0].message.content or ""}
