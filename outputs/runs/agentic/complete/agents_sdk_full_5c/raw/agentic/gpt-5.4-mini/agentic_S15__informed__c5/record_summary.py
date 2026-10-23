from __future__ import annotations

from typing import Any, Dict, Iterable

from openai import OpenAI

from database_models import NormalizedResponse

MODEL_ID = "gpt-4.1-mini"


def summarize_records(records: Iterable[Dict[str, Any]], prompt: str = "Summarize the key details in these records.") -> NormalizedResponse:
    client = OpenAI()
    text = "\n".join(str(record) for record in records)
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    )
    content = response.choices[0].message.content if response.choices else ""
    return NormalizedResponse(ok=True, data={"summary": content, "model": MODEL_ID})
