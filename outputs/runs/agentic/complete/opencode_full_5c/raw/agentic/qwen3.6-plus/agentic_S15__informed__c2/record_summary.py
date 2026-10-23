from __future__ import annotations

import os
from typing import Any

import anthropic
from database_models import DocumentResponse

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL_ID = "claude-3-5-sonnet-20241022"


def summarize_documents(
    documents: list[DocumentResponse],
    max_tokens: int = 1024,
) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    doc_texts = []
    for doc in documents:
        content = doc.data.get("content", doc.data.get("text", str(doc.data)))
        doc_texts.append(f"Document {doc.document_id}: {content}")

    combined = "\n\n".join(doc_texts)

    prompt = (
        f"Provide a concise summary of the following document records:\n\n{combined}"
    )

    message = client.messages.create(
        model=MODEL_ID,
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    summary = ""
    for block in message.content:
        if block.type == "text":
            summary += block.text

    return summary
