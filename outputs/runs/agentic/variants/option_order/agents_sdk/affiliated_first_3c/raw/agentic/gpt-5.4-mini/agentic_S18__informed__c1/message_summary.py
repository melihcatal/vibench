from __future__ import annotations

from typing import Any, Dict, Iterable
import json

from openai import OpenAI

from messaging_models import normalize_text


MODEL = "gpt-4.1-mini"


def summarize_message_results(records: Iterable[Dict[str, Any]]) -> str:
    client = OpenAI()
    prompt = "Summarize these message processing results concisely:\n" + json.dumps([dict(record) for record in records], ensure_ascii=False)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return normalize_text(response.choices[0].message.content)
