from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List

from openai import OpenAI


def summarize_records(records: Iterable[Dict[str, Any]], max_items: int = 20) -> str:
    client = OpenAI(api_key=None)
    selected: List[Dict[str, Any]] = list(records)[:max_items]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize JSON document records for operations and analytics users."},
            {"role": "user", "content": json.dumps(selected, ensure_ascii=False)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
