import os
from typing import Any, Dict, List, Optional

import anthropic
from anthropic import Anthropic

from database_models import DocumentResponse


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")


def summarize_documents(
    documents: List[Dict[str, Any]],
    summary_type: str = "overview",
    max_tokens: int = 1024,
) -> DocumentResponse:
    if not documents:
        return DocumentResponse(
            success=False,
            error="No documents provided for summarization",
        )

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    doc_contents = []
    for i, doc in enumerate(documents):
        doc_id = doc.get("id", doc.get("_id", f"doc_{i}"))
        content_fields = {
            k: v
            for k, v in doc.items()
            if k
            not in ("_id", "id", "created_at", "updated_at", "partition_key", "version")
        }
        doc_contents.append(f"Document {doc_id}: {content_fields}")

    combined_text = "\n\n".join(doc_contents)

    system_prompt = (
        "You are a document summarization assistant. Provide a concise, structured summary "
        "of the provided document records. Focus on key information, patterns, and notable content."
    )

    if summary_type == "overview":
        user_prompt = (
            f"Provide a high-level overview summary of the following {len(documents)} document records:\n\n"
            f"{combined_text}"
        )
    elif summary_type == "key_points":
        user_prompt = (
            f"Extract the key points and important details from the following {len(documents)} document records:\n\n"
            f"{combined_text}"
        )
    elif summary_type == "comparison":
        user_prompt = (
            f"Compare and contrast the following {len(documents)} document records, "
            f"highlighting similarities and differences:\n\n"
            f"{combined_text}"
        )
    else:
        user_prompt = (
            f"Summarize the following {len(documents)} document records:\n\n"
            f"{combined_text}"
        )

    try:
        message = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        summary_text = ""
        for block in message.content:
            if hasattr(block, "text"):
                summary_text += block.text

        return DocumentResponse(
            success=True,
            document={
                "summary_type": summary_type,
                "document_count": len(documents),
                "summary": summary_text,
                "model": ANTHROPIC_MODEL,
            },
        )
    except Exception as exc:
        return DocumentResponse(
            success=False,
            error=f"Summarization error via Anthropic Messages API: {exc}",
        )
