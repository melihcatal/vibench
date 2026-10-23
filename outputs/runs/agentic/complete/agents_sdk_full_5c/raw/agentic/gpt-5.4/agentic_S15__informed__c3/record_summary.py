from __future__ import annotations

import json
import os
from typing import Any, Iterable, Mapping

from openai import OpenAI


MODEL_NAME = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")



def _records_to_text(records: Iterable[Mapping[str, Any]]) -> str:
    return json.dumps(list(records), ensure_ascii=False, indent=2, default=str)



def summarize_records(records: Iterable[Mapping[str, Any]]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = _records_to_text(records)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "Summarize document records for operations staff. Highlight IDs, statuses, ownership, timestamps, and notable anomalies."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
