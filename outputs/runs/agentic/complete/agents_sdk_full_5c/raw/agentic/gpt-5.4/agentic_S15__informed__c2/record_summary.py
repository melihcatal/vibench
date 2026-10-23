from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")



def summarize_records(records: Iterable[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    payload: List[Dict[str, Any]] = [dict(record) for record in records]
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Summarize document-store records for an internal operations report."},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
