from __future__ import annotations

import os

from openai import OpenAI

from storage_models import StoredAssetSummaryResult


def summarize_stored_asset_content(
    text: str, metadata: dict | None = None
) -> StoredAssetSummaryResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = "gpt-4o-mini"
    metadata_text = ""
    if metadata:
        metadata_text = "Metadata: " + ", ".join(
            f"{k}={v}" for k, v in metadata.items()
        )
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Summarize stored asset content in a concise paragraph for search and review.",
            },
            {
                "role": "user",
                "content": f"{metadata_text}\n\nContent:\n{text}",
            },
        ],
    )
    return StoredAssetSummaryResult(
        summary=response.output_text,
        provider="openai",
        model=model,
    )
