from __future__ import annotations

from storage_client import get_openai_client
from storage_models import SummaryResult


def summarize_stored_asset_text(
    extracted_text: str, metadata: dict[str, str] | None = None
) -> SummaryResult:
    client = get_openai_client()
    metadata_lines = "\n".join(f"{k}: {v}" for k, v in sorted((metadata or {}).items()))
    prompt = f"Summarize the stored asset content for retrieval and review.\nMetadata:\n{metadata_lines}\n\nContent:\n{extracted_text}"
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        max_output_tokens=220,
    )
    summary = response.output_text
    return SummaryResult(summary=summary, model="gpt-4.1-mini")
