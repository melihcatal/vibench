from __future__ import annotations

from openai import OpenAI

from storage_client import get_openai_api_key
from storage_models import SummaryResult


OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def summarize_stored_asset_content(extracted_text: str, metadata: dict | None = None) -> SummaryResult:
    client = OpenAI(api_key=get_openai_api_key())
    metadata = metadata or {}
    prompt = (
        "Summarize the following stored asset content for catalog search and review. "
        "Return a concise paragraph and preserve important entities and numbers.\n\n"
        f"Metadata: {metadata}\n\n"
        f"Content:\n{extracted_text}"
    )
    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "You summarize enterprise document content."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    summary = response.choices[0].message.content or ""
    return SummaryResult(summary=summary.strip(), model=OPENAI_SUMMARY_MODEL)
