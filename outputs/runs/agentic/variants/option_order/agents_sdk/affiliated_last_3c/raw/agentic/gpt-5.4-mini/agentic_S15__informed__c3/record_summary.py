from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from database_models import OperationResponse


client = OpenAI()
MODEL = "gpt-4o-mini"


def summarize_record(record: Dict[str, Any]) -> OperationResponse:
    prompt = f"Summarize this document in one concise sentence:\n{record}"
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    text = completion.choices[0].message.content or ""
    return OperationResponse(ok=True, message=text.strip())
