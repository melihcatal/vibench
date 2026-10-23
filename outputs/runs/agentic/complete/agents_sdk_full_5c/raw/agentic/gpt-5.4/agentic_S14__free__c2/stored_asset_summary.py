from __future__ import annotations

import os

from openai import OpenAI

from storage_models import SummaryResult


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_asset_content(extracted_text: str, metadata: dict | None = None) -> SummaryResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    context = ""
    if metadata:
        context = f"Metadata: {metadata}\n\n"
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=(
            "Summarize the stored asset content for search and review. "
            "Return a concise paragraph and key facts inline.\n\n"
            f"{context}"
            f"Content:\n{extracted_text}"
        ),
    )
    return SummaryResult(summary=response.output_text, model=OPENAI_MODEL)
