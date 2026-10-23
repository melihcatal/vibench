from __future__ import annotations

import os
from typing import Iterable, Mapping, Any

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_records(records: Iterable[Mapping[str, Any]]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    lines = []
    for record in records:
        lines.append(str(dict(record)))
    prompt = "Summarize these managed document store records for an operations dashboard:\n" + "\n".join(lines)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        max_output_tokens=180,
    )
    return response.output_text
