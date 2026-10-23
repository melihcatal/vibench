from __future__ import annotations

from openai import OpenAI

from storage_client import require_openai_api_key
from storage_models import SummaryResult


def summarize_asset_content(
    text: str, metadata: dict[str, str] | None = None
) -> SummaryResult:
    client = OpenAI(api_key=require_openai_api_key())
    metadata_text = "\n".join(f"{k}: {v}" for k, v in (metadata or {}).items())
    prompt = f"Summarize the following stored asset content clearly and concisely.\nMetadata:\n{metadata_text}\n\nContent:\n{text}"
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return SummaryResult(summary=response.output_text, model="gpt-4.1-mini")
