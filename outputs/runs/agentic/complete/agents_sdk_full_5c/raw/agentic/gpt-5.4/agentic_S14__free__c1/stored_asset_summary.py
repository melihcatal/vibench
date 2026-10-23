from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from storage_models import SummaryResult


DEFAULT_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_asset_text(text: str, model: Optional[str] = None) -> SummaryResult:
    if not text.strip():
        raise ValueError("text must not be empty")

    resolved_model = model or DEFAULT_MODEL
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=resolved_model,
        input=[
            {
                "role": "system",
                "content": "You summarize OCR or extracted document content into a concise asset summary.",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        max_output_tokens=220,
    )
    return SummaryResult(
        provider="openai",
        model=resolved_model,
        summary=response.output_text,
    )
