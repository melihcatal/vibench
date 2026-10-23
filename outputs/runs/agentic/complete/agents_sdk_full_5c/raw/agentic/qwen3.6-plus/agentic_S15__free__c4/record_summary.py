"""
Summarize retrieved document records using OpenAI GPT-4 Turbo.
Uses the OpenAI API for managed document record summarization.
"""

from __future__ import annotations

import json
import os
from typing import Any, Optional

import openai
from openai import OpenAI

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL_ID = "gpt-4-turbo"
SUMMARIZATION_PROMPT = (
    "You are a document summarization assistant. Given the following document records "
    "from a NoSQL document store, produce a concise summary highlighting the key points, "
    "status, and any notable patterns across the records. Format the summary as a "
    "structured JSON object with the keys: 'overview', 'key_points' (list of strings), "
    "'status_distribution' (dict of status -> count), and 'notable_patterns' (list of strings)."
)


def _get_openai_client() -> OpenAI:
    """Create and return an OpenAI client configured with the API key from environment."""
    api_key = os.environ.get(OPENAI_API_KEY_ENV)
    if not api_key:
        raise EnvironmentError(f"Environment variable {OPENAI_API_KEY_ENV} is not set.")
    return OpenAI(api_key=api_key)


def summarize_records(
    records: list[dict[str, Any]],
    model: str = OPENAI_MODEL_ID,
    max_tokens: int = 1024,
    client: Optional[OpenAI] = None,
) -> dict[str, Any]:
    """
    Summarize a list of retrieved document records using OpenAI GPT-4 Turbo.
    
    Args:
        records: A list of document record dicts (e.g., from fetch_document or query_documents).
        model: The OpenAI model identifier to use (default: gpt-4-turbo).
        max_tokens: Maximum tokens in the generated summary.
        client: Optional pre-configured OpenAI client instance.
    
    Returns:
        A dict containing the parsed JSON summary from OpenAI.
    """
    if client is None:
        client = _get_openai_client()

    records_json = json.dumps(records, indent=2, default=str)
    user_message = f"Document records to summarize:\n{records_json}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SUMMARIZATION_PROMPT},
            {"role": "user", "content": user_message},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    summary_text = response.choices[0].message.content
    if summary_text is None:
        raise RuntimeError("OpenAI GPT-4 Turbo returned an empty summary response.")

    try:
        return json.loads(summary_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Failed to parse OpenAI GPT-4 Turbo summary as JSON: {e}\nRaw: {summary_text}"
        )


def summarize_single_record(
    record: dict[str, Any],
    model: str = OPENAI_MODEL_ID,
    client: Optional[OpenAI] = None,
) -> str:
    """
    Generate a brief textual summary of a single document record using OpenAI GPT-4 Turbo.
    
    Args:
        record: A single document record dict.
        model: The OpenAI model identifier (default: gpt-4-turbo).
        client: Optional pre-configured OpenAI client instance.
    
    Returns:
        A string containing the generated summary.
    """
    if client is None:
        client = _get_openai_client()

    record_json = json.dumps(record, indent=2, default=str)
    user_message = (
        f"Provide a concise one-paragraph summary of the following document record:\n{record_json}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a document summarization assistant. Provide concise, factual summaries."},
            {"role": "user", "content": user_message},
        ],
        max_tokens=256,
        temperature=0.2,
    )

    summary = response.choices[0].message.content
    if summary is None:
        raise RuntimeError("OpenAI GPT-4 Turbo returned an empty summary.")
    return summary


if __name__ == "__main__":
    sample_records = [
        {
            "doc_id": "doc-001",
            "content": {"title": "Quarterly Report Q1", "status": "finalized", "author": "Alice"},
        },
        {
            "doc_id": "doc-002",
            "content": {"title": "Quarterly Report Q2", "status": "draft", "author": "Bob"},
        },
    ]
    result = summarize_records(sample_records)
    print(json.dumps(result, indent=2))
