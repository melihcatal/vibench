"""
[LATER-STEP] record_summary.py
Summarize retrieved document records using OpenAI GPT via the OpenAI Chat Completions API.
Provider: OpenAI / Azure OpenAI chat completions via openai SDK.
Auth: OPENAI_API_KEY
"""

import os
from typing import List, Dict, Any

from openai import OpenAI
from database_models import DocumentResponse


def summarize_records(
    documents: List[Dict[str, Any]],
    model: str = "gpt-4o-mini",
    max_tokens: int = 500,
) -> str:
    """
    Generate a concise summary of a list of document records using OpenAI's GPT model.

    Args:
        documents: A list of document dictionaries (typically from DocumentResponse.to_dict()).
        model: The OpenAI model identifier to use (default: gpt-4o-mini).
        max_tokens: Maximum tokens for the generated summary.

    Returns:
        A string containing the generated summary.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)

    records_text = ""
    for i, doc in enumerate(documents, 1):
        doc_id = doc.get("document_id", "unknown")
        data = doc.get("data", {})
        title = data.get("title", "Untitled")
        body = data.get("body", "")
        records_text += f"\nRecord {i} (ID: {doc_id}):\n  Title: {title}\n  Content: {body}\n"

    system_prompt = (
        "You are a document summarization assistant. "
        "Summarize the provided document records concisely, highlighting key topics and themes."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Summarize these document records:\n{records_text}"},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    return response.choices[0].message.content


def summarize_document_responses(
    responses: List[DocumentResponse],
    model: str = "gpt-4o-mini",
) -> str:
    """
    Convenience wrapper that accepts DocumentResponse objects directly.

    Args:
        responses: A list of DocumentResponse objects.
        model: The OpenAI model identifier to use.

    Returns:
        A string containing the generated summary.
    """
    doc_dicts = [r.to_dict() for r in responses]
    return summarize_records(doc_dicts, model=model)


if __name__ == "__main__":
    sample_docs = [
        {
            "document_id": "doc-001",
            "data": {"title": "Meeting Notes Q1", "body": "Discussed roadmap and budget."},
        },
        {
            "document_id": "doc-002",
            "data": {"title": "Project Plan", "body": "Sprint schedule and milestones defined."},
        },
    ]
    summary = summarize_records(sample_docs)
    print(summary)
