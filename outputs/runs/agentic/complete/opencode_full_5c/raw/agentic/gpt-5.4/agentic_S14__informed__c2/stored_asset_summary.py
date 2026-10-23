from __future__ import annotations

import os

from openai import OpenAI

from storage_models import AssetSummaryResult


def summarize_asset_text(
    extracted_text: str, metadata: dict[str, str] | None = None
) -> AssetSummaryResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    metadata_items = metadata or {}
    prompt = f"Metadata: {metadata_items}\n\nContent:\n{extracted_text}\n\nSummarize the asset for indexing and review in 5 sentences or fewer."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You summarize stored business documents succinctly.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    summary = response.choices[0].message.content or ""
    return AssetSummaryResult(summary=summary, model="gpt-4o-mini", provider="openai")
