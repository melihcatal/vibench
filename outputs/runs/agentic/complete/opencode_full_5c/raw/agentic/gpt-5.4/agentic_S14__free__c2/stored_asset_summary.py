from __future__ import annotations

from openai import OpenAI

from storage_client import get_openai_api_key
from storage_models import SummaryResult


def summarize_stored_asset_text(text: str) -> SummaryResult:
    client = OpenAI(api_key=get_openai_api_key())
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize extracted asset text concisely for downstream search and review.",
            },
            {"role": "user", "content": text},
        ],
    )
    summary = response.output_text
    return SummaryResult(summary=summary, model="gpt-4.1-mini", provider="openai")
