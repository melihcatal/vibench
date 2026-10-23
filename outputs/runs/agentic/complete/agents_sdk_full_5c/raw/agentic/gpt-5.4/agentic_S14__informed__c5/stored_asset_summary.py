from __future__ import annotations

from openai import OpenAI

from storage_models import SummaryResult

OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def summarize_asset_text(text: str, max_words: int = 150) -> SummaryResult:
    client = OpenAI()
    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You summarize extracted document content for enterprise asset indexing.",
            },
            {
                "role": "user",
                "content": f"Summarize the following content in at most {max_words} words:\n\n{text}",
            },
        ],
        temperature=0.2,
    )
    summary = response.choices[0].message.content or ""
    return SummaryResult(provider="openai", model=OPENAI_SUMMARY_MODEL, summary=summary.strip())
