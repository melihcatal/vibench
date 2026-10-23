from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


OPENAI_MODEL = os.environ.get("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def record_summary(records: Iterable[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    payload: List[Dict[str, Any]] = list(records)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": "Summarize managed NoSQL document records into concise operational notes."},
            {"role": "user", "content": str(payload)},
        ],
    )
    return response.output_text
