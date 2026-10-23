from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def vendor_text_safety(text: str) -> Dict[str, Any]:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Assess vendor text for unsafe or disallowed content and return JSON."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return {"provider": "openai", "model": MODEL_ID, "result": completion.choices[0].message.content or ""}
