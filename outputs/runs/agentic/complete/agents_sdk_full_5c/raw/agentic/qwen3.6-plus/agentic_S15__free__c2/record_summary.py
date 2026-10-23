"""
Summarize retrieved document records using OpenAI's gpt-4o model.
Uses the official openai Python SDK to call the OpenAI Chat Completions API.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from database_models import DocumentResponse, DocumentListResponse


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL_ID = "gpt-4o"
OPENAI_MODEL_FAMILY = "gpt-4"


def summarize_document(
    document: DocumentResponse,
    max_tokens: int = 256,
    temperature: float = 0.3,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Generate a concise summary of a single retrieved document using OpenAI gpt-4o.

    Args:
        document: The DocumentResponse to summarize.
        max_tokens: Maximum tokens for the summary.
        temperature: Sampling temperature for the OpenAI model.
        client: Optional pre-configured OpenAI client instance.

    Returns:
        Dict with keys: document_id, summary, model_used.
    """
    if client is None:
        api_key = os.environ.get(OPENAI_API_KEY_ENV)
        if not api_key:
            raise EnvironmentError(f"Missing environment variable: {OPENAI_API_KEY_ENV}")
        client = OpenAI(api_key=api_key)

    doc_content = json.dumps(document.data, indent=2, default=str)

    prompt = (
        "Summarize the following JSON document in 3-5 sentences. "
        "Focus on the key data points, purpose, and any notable fields.\n\n"
        f"Document JSON:\n{doc_content}"
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL_ID,
        messages=[
            {"role": "system", "content": "You are a document summarization assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    summary_text = response.choices[0].message.content.strip()

    return {
        "document_id": document.id,
        "summary": summary_text,
        "model_used": OPENAI_MODEL_ID,
        "model_family": OPENAI_MODEL_FAMILY,
    }


def summarize_document_batch(
    documents: List[DocumentResponse],
    max_tokens: int = 256,
    temperature: float = 0.3,
    client: Optional[OpenAI] = None,
) -> List[Dict[str, Any]]:
    """
    Summarize a list of DocumentResponse objects using OpenAI gpt-4o.

    Args:
        documents: List of DocumentResponse objects to summarize.
        max_tokens: Maximum tokens per summary.
        temperature: Sampling temperature.
        client: Optional pre-configured OpenAI client.

    Returns:
        List of summary dicts, one per document.
    """
    summaries = []
    for doc in documents:
        summary = summarize_document(
            document=doc,
            max_tokens=max_tokens,
            temperature=temperature,
            client=client,
        )
        summaries.append(summary)
    return summaries


if __name__ == "__main__":
    sample_doc = DocumentResponse(
        id="doc-001",
        data={
            "title": "Q4 Revenue Report",
            "department": "Finance",
            "content": "Total revenue for Q4 was $4.2M, up 12% YoY. Key drivers included enterprise SaaS subscriptions and professional services. Customer churn decreased to 2.1%.",
            "tags": ["finance", "quarterly", "revenue"],
        },
        metadata={"version": 1},
    )
    result = summarize_document(sample_doc)
    print(json.dumps(result, indent=2))
