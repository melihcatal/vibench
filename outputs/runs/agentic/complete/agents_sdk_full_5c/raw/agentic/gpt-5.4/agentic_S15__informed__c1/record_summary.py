from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_records(records: Iterable[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    payload: List[Dict[str, Any]] = list(records)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You summarize managed document-store records into concise operational prose.",
            },
            {
                "role": "user",
                "content": "Summarize these JSON records, highlighting trends, anomalies, and notable user-facing content:\n"
                + json.dumps(payload, ensure_ascii=False),
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
