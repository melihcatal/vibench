"""
Summarize retrieved document records using the OpenAI Chat Completions API.

Uses the openai SDK to call GPT models for generating concise summaries
of document content. Requires OPENAI_API_KEY environment variable.

Concrete model: gpt-4o (OpenAI)
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional

from openai import OpenAI


def summarize_documents(
    documents: List[Dict[str, Any]],
    model: str = "gpt-4o",
    max_tokens: int = 500,
    temperature: float = 0.3,
    fields: Optional[List[str]] = None,
    language: str = "en",
) -> Dict[str, Any]:
    """Summarize one or more document records using OpenAI's GPT model.

    Args:
        documents: List of document dicts to summarize.
        model: OpenAI model identifier (default: gpt-4o).
        max_tokens: Maximum tokens in the summary response.
        temperature: Sampling temperature for the generation.
        fields: Specific fields to extract from each document for summarization.
        language: Language code for the summary output.

    Returns:
        Dict with 'success', 'summaries', and optional 'error' keys.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "OPENAI_API_KEY environment variable is required",
            "summaries": [],
        }

    client = OpenAI(api_key=api_key)

    text_segments = []
    for idx, doc in enumerate(documents):
        doc_id = doc.get("doc_id", doc.get("document_id", f"doc-{idx}"))
        content_parts = []

        if fields:
            for field in fields:
                val = doc.get(field)
                if val:
                    content_parts.append(f"{field}: {val}")
        else:
            for key, val in doc.items():
                if key in ("doc_id", "document_id", "version", "metadata", "ttl"):
                    continue
                if isinstance(val, str) and val.strip():
                    content_parts.append(f"{key}: {val}")

        if content_parts:
            text_segments.append(f"[Document: {doc_id}]\n" + "\n".join(content_parts))

    if not text_segments:
        return {
            "success": False,
            "error": "No content found in documents to summarize",
            "summaries": [],
        }

    combined_text = "\n\n---\n\n".join(text_segments)

    system_prompt = (
        "You are a document summarization assistant. Provide clear, concise "
        "summaries of the provided document records. Include key information "
        f"and maintain the original meaning. Respond in {language}."
    )

    user_prompt = (
        f"Please summarize the following {len(documents)} document(s):\n\n{combined_text}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        summary_text = response.choices[0].message.content
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }

        return {
            "success": True,
            "summaries": [
                {
                    "source_count": len(documents),
                    "summary": summary_text,
                    "model": model,
                }
            ],
            "usage": usage,
        }
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "summaries": [],
        }


def summarize_single_document(
    document: Dict[str, Any],
    model: str = "gpt-4o",
    fields: Optional[List[str]] = None,
    language: str = "en",
) -> Dict[str, Any]:
    """Convenience wrapper to summarize a single document."""
    return summarize_documents(
        documents=[document],
        model=model,
        fields=fields,
        language=language,
    )


if __name__ == "__main__":
    raw_input = sys.stdin.read() if not sys.stdin.isatty() else ""

    if raw_input:
        data = json.loads(raw_input)
    else:
        data = {
            "documents": [
                {
                    "doc_id": "doc-001",
                    "title": "Quarterly Report Q3 2024",
                    "content": "Revenue increased by 15% compared to the previous quarter. "
                    "Key drivers included new product launches and expansion into European markets. "
                    "Operating expenses remained stable at $2.1M.",
                    "status": "published",
                }
            ],
            "model": "gpt-4o",
            "language": "en",
        }

    result = summarize_documents(
        documents=data.get("documents", []),
        model=data.get("model", "gpt-4o"),
        max_tokens=data.get("max_tokens", 500),
        temperature=data.get("temperature", 0.3),
        fields=data.get("fields"),
        language=data.get("language", "en"),
    )
    print(json.dumps(result, indent=2))
