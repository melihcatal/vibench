from __future__ import annotations

from openai import OpenAI

from storage_client import get_openai_api_key
from storage_models import SummaryResult


OPENAI_MODEL = "gpt-4o-mini"


def summarize_stored_asset_text(extracted_text: str) -> SummaryResult:
    client = OpenAI(api_key=get_openai_api_key())
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize stored asset text into a concise search-friendly paragraph.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": extracted_text}],
            },
        ],
    )
    return SummaryResult(
        summary=response.output_text,
        model=OPENAI_MODEL,
        provider="OpenAI",
    )
