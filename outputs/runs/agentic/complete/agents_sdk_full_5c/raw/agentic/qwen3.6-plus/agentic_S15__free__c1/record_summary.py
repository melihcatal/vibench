"""
record_summary.py - Summarizes retrieved document records using
OpenAI's GPT-4o model for text summarization.

Provider: OpenAI API (api.openai.com) - concrete model: gpt-4o
"""

import os
from typing import Any, Dict, List

import openai
from openai import OpenAI

from database_models import DocumentRecord, extract_user_facing_fields

# OpenAI provider-specific configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL_ID = os.environ.get("OPENAI_MODEL_ID", "gpt-4o")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")


def summarize_record(record: DocumentRecord) -> str:
    """
    Generate a concise summary of a document record using OpenAI GPT-4o.
    Extracts user-facing fields from the record and sends them to the
    OpenAI API for summarization.
    """
    user_fields = extract_user_facing_fields(record)
    if not user_fields:
        return f"[No user-facing text found in document '{record.doc_id}']"

    content_parts = []
    for field_name, text in user_fields.items():
        content_parts.append(f"{field_name}: {text}")

    prompt_text = "\n---\n".join(content_parts)

    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document summarization assistant. "
                    "Produce a concise, factual summary of the provided document "
                    "fields. Keep the summary to 2-3 sentences maximum."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Summarize the following document fields:\n\n{prompt_text}"
                ),
            },
        ],
        max_tokens=300,
        temperature=0.3,
    )

    summary = response.choices[0].message.content
    return summary or "[Empty summary from OpenAI gpt-4o]"


def summarize_records(records: List[DocumentRecord]) -> Dict[str, str]:
    """
    Summarize multiple document records using OpenAI GPT-4o.
    Returns a mapping of doc_id to its summary text.
    """
    results: Dict[str, str] = {}
    for record in records:
        results[record.doc_id] = summarize_record(record)
    return results
