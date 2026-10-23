from __future__ import annotations

from openai import OpenAI

from storage_client import openai_api_key
from storage_models import SummaryResult


OPENAI_SUMMARY_MODEL = "gpt-4.1-mini"


def summarize_stored_asset_text(text: str) -> SummaryResult:
    client = OpenAI(api_key=openai_api_key())
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize extracted asset text concisely for downstream search and review.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": text}],
            },
        ],
    )
    return SummaryResult(
        source_text=text,
        summary=response.output_text,
        model=OPENAI_SUMMARY_MODEL,
        provider="openai",
    )
