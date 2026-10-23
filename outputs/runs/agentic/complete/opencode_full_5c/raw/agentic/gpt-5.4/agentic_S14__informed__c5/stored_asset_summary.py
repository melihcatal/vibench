from __future__ import annotations

from openai import OpenAI

from storage_models import SummaryResult


def summarize_stored_asset_content(text: str) -> SummaryResult:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize stored asset content in a concise paragraph.",
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
        summary=response.output_text,
        provider="openai",
        model="gpt-4.1-mini",
    )
