from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from storage_models import SummaryResult


_DEFAULT_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_asset_text(extracted_text: str, metadata_context: Optional[dict] = None) -> SummaryResult:
    if not extracted_text.strip():
        raise ValueError("Extracted text is required for OpenAI summarization")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Summarize the following stored asset content for search, review, and routing."
    if metadata_context:
        prompt += f"\nMetadata: {metadata_context}"

    response = client.responses.create(
        model=_DEFAULT_MODEL,
        input=[
            {"role": "system", "content": "You create concise factual summaries."},
            {"role": "user", "content": f"{prompt}\n\nContent:\n{extracted_text}"},
        ],
    )
    return SummaryResult(
        provider="OpenAI",
        model=_DEFAULT_MODEL,
        summary=response.output_text,
        raw=response.model_dump(),
    )
