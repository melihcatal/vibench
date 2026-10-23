from __future__ import annotations

import os

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"


def moderate_claim_text(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Assess whether identity-provider claims notes contain risky or abusive text."},
            {"role": "user", "content": text},
        ],
    )
    return {"model": OPENAI_MODEL, "result": completion.choices[0].message.content}
