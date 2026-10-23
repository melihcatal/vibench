"""
Summarize retrieved document records using OpenAI GPT-4o-mini.
"""

import os
import json

from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini-2024-07-18"


def summarize_records(records: list[dict]) -> str:
    """
    Generate a concise summary of a list of document records.

    Parameters
    ----------
    records : list[dict]
        Parsed document records, each expected to contain at least a
        ``document_id`` key and arbitrary text-bearing fields.

    Returns
    -------
    str
        Human-readable summary of the provided records.
    """
    if not records:
        return "No records to summarize."

    client = OpenAI(api_key=OPENAI_API_KEY)

    formatted = []
    for idx, rec in enumerate(records, start=1):
        snippet = json.dumps(rec, default=str, ensure_ascii=False)
        formatted.append(f"Record {idx}: {snippet}")

    system_prompt = (
        "You are a document analysis assistant. Summarize the provided document records "
        "into a concise paragraph highlighting key topics, common fields, and notable details."
    )
    user_content = "Summarize the following document records:\n\n" + "\n\n".join(formatted)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    summary = response.choices[0].message.content.strip() if response.choices else ""
    return summary
