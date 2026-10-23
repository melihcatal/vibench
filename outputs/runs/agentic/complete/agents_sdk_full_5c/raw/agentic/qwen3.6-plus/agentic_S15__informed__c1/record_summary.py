"""
Summarize retrieved document records using Mistral Chat API.
Connects to the Mistral hosted LLM inference service to generate
concise summaries of document data.
"""

import os
import json
from typing import Dict, List, Optional

from mistralai import Mistral


MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "")
MISTRAL_MODEL = "mistral-large-latest"


def build_summary_prompt(documents: List[Dict[str, str]]) -> str:
    """Build a prompt from document data for summarization."""
    lines = []
    for i, doc in enumerate(documents, 1):
        text_content = doc.get("content", doc.get("text", json.dumps(doc)))
        lines.append(f"Document {i}: {text_content}")
    joined = "\n\n".join(lines)
    return (
        "Summarize the following documents concisely. "
        "Provide a brief overview of the key points across all documents.\n\n"
        f"{joined}"
    )


def summarize_documents(
    documents: List[Dict[str, str]],
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> str:
    """
    Summarize a list of document records using the Mistral Chat API.

    Args:
        documents: List of dicts, each containing document fields like 'content'
                   or 'text'.
        max_tokens: Maximum tokens for the generated summary.
        temperature: Sampling temperature for the Mistral model.

    Returns:
        A string containing the generated summary.
    """
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY environment variable is required")

    client = Mistral(api_key=MISTRAL_API_KEY)
    prompt = build_summary_prompt(documents)

    response = client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes documents clearly and concisely.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    summary = response.choices[0].message.content
    return summary if summary is not None else ""


def summarize_single_document(
    document_data: Dict[str, str],
    max_tokens: int = 256,
    temperature: float = 0.3,
) -> str:
    """Summarize a single document record via Mistral."""
    return summarize_documents(
        [document_data], max_tokens=max_tokens, temperature=temperature
    )
