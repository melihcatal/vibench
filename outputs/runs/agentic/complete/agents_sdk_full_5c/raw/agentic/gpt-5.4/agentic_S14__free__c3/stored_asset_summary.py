from __future__ import annotations

import os

from openai import OpenAI

from storage_models import SummaryResult



def summarize_asset_text(text: str, metadata: dict | None = None) -> SummaryResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")
    metadata_text = ""
    if metadata:
        metadata_text = "\nMetadata: " + ", ".join(f"{k}={v}" for k, v in metadata.items())
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "You summarize stored business documents into a concise paragraph and bullet highlights.",
            },
            {
                "role": "user",
                "content": f"Summarize this stored asset content for downstream search and review:{metadata_text}\n\n{text}",
            },
        ],
    )
    return SummaryResult(
        summary=response.output_text,
        model=model,
        provider_response_id=response.id,
    )
