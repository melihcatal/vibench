import os
from typing import Any, Dict, List

from openai import OpenAI


MODEL_ID = "gpt-5.4-mini"


def _normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": record.get("id"),
        "title": record.get("title") or record.get("name") or record.get("filename"),
        "summary": record.get("summary") or record.get("content") or record.get("text"),
        "metadata": record.get("metadata") or {},
    }


def summarize_records(records: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    normalized = [_normalize_record(record) for record in records]
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "system",
                "content": "Summarize retrieved document records concisely, highlighting shared themes, key entities, and notable differences.",
            },
            {
                "role": "user",
                "content": f"Records:\n{normalized}",
            },
        ],
    )
    return response.output_text


def summarize_record(record: Dict[str, Any]) -> str:
    return summarize_records([record])


if __name__ == "__main__":
    raise SystemExit("Import and call summarize_records() with retrieved document records.")
