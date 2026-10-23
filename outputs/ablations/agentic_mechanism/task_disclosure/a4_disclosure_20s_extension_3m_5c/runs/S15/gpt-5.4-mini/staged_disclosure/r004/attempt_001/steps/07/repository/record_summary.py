import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def _format_record(record: Dict[str, Any], index: int) -> str:
    parts = [f"Record {index}"]
    for key in sorted(record.keys()):
        value = record[key]
        if value is None:
            continue
        parts.append(f"{key}: {value}")
    return "\n".join(parts)


def summarize_records(records: Iterable[Dict[str, Any]]) -> str:
    records_list = list(records)
    if not records_list:
        return "No records provided."

    payload = "\n\n".join(_format_record(record, i + 1) for i, record in enumerate(records_list))

    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You summarize retrieved document records concisely, focusing on shared themes, notable entities, and any gaps or anomalies.",
            },
            {
                "role": "user",
                "content": f"Summarize these retrieved document records:\n\n{payload}",
            },
        ],
    )

    return response.output_text.strip()


def summarize_document_record(record: Dict[str, Any]) -> str:
    return summarize_records([record])


if __name__ == "__main__":
    sample_records = [
        {"id": 1, "title": "Quarterly Report", "status": "final", "department": "Finance"},
        {"id": 2, "title": "Meeting Notes", "status": "draft", "department": "Operations"},
    ]
    print(summarize_records(sample_records))
