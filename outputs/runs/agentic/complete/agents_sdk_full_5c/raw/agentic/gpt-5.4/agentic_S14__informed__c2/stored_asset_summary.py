from __future__ import annotations

import os

from openai import OpenAI

from storage_models import SummaryResult


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_asset_content(extracted_text: str, metadata: dict[str, str] | None = None, max_output_tokens: int = 220) -> SummaryResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    metadata_text = "\n".join(f"{k}: {v}" for k, v in (metadata or {}).items())
    prompt = (
        "Summarize the stored asset for search and review. Focus on key entities, topics, and any actionable items.\n"
        f"Metadata:\n{metadata_text or 'None'}\n\n"
        f"Extracted text:\n{extracted_text}"
    )
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        max_output_tokens=max_output_tokens,
    )
    return SummaryResult(summary=response.output_text, model=OPENAI_MODEL)


def summarize_asset_content_dict(extracted_text: str, metadata: dict[str, str] | None = None) -> dict:
    return summarize_asset_content(extracted_text=extracted_text, metadata=metadata).to_dict()
