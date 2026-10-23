from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

PROVIDER_NAME = "openai"
MODEL_ID = "gpt-4o-mini"


def moderate_vendor_text(text: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Classify whether vendor text contains safety issues, harassment, or policy concerns."},
            {"role": "user", "content": text},
        ],
        temperature=0.0,
    )
    content = response.choices[0].message.content or ""
    return {"provider": PROVIDER_NAME, "model": MODEL_ID, "result": content}
