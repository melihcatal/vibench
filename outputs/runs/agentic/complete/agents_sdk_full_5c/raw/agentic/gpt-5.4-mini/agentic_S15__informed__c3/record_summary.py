from __future__ import annotations

from typing import Any, Dict, Iterable, List

from openai import OpenAI

SUMMARY_MODEL = "gpt-4o-mini"


def summarize_records(records: Iterable[Dict[str, Any]]) -> str:
    client = OpenAI()
    prompt = "Summarize the following document records briefly and accurately:\n" + "\n".join([str(record) for record in records])
    completion = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "You summarize document records."},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content or ""
