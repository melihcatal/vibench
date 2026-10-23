from __future__ import annotations

from openai import OpenAI

from storage_models import SummaryResult


OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def summarize_asset_text(text: str, max_chars: int = 12000) -> SummaryResult:
    client = OpenAI()
    prompt = text[:max_chars]
    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You summarize OCR-extracted document content into a concise operational summary.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    summary = response.choices[0].message.content or ""
    return SummaryResult(summary=summary, model=OPENAI_SUMMARY_MODEL, provider="openai")
