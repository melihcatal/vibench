from __future__ import annotations

import os

from openai import OpenAI

from storage_models import AssetSummaryResult


def summarize_asset_content(
    extracted_text: str, metadata: dict[str, str] | None = None
) -> AssetSummaryResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    metadata_text = ""
    if metadata:
        metadata_text = "\n".join(f"{key}: {value}" for key, value in metadata.items())
    prompt = f"Metadata:\n{metadata_text}\n\nContent:\n{extracted_text}\n\nProvide a concise summary of the stored asset."
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return AssetSummaryResult(
        provider="openai",
        model="gpt-4.1-mini",
        summary=response.output_text,
    )
