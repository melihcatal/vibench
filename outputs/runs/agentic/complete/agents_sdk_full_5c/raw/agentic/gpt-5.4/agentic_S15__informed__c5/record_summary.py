from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")



def summarize_records(records: Iterable[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    material: List[Dict[str, Any]] = list(records)
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize document-store records into a concise operational summary.",
            },
            {
                "role": "user",
                "content": json.dumps(material, ensure_ascii=False),
            },
        ],
    )
    return response.output_text.strip()
