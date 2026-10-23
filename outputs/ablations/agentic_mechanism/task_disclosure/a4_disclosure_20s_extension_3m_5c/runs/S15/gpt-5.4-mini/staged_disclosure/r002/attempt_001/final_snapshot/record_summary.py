import os
from typing import Any, Dict, List

from openai import OpenAI


MODEL = "openai/gpt-5.4-mini"


def _normalize_record(record: Any) -> str:
    if isinstance(record, str):
        return record.strip()
    if isinstance(record, dict):
        parts: List[str] = []
        for key in sorted(record.keys()):
            value = record[key]
            parts.append(f"{key}: {value}")
        return " | ".join(parts)
    return str(record).strip()


def summarize_records(records: List[Any]) -> str:
    if not records:
        return "No records provided."

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    content = "\n".join(f"- {_normalize_record(record)}" for record in records)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Summarize retrieved document records concisely, highlighting key themes, entities, and notable differences.",
            },
            {"role": "user", "content": content},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def summarize_record_batch(records: List[Dict[str, Any]]) -> str:
    return summarize_records(records)
