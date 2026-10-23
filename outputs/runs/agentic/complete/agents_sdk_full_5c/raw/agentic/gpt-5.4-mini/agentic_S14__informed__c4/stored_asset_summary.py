from __future__ import annotations

from openai import OpenAI

from storage_models import SummaryResult

MODEL_ID = "gpt-4o-mini"


def stored_asset_summary(text: str) -> SummaryResult:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize the provided asset text concisely."},
            {"role": "user", "content": text},
        ],
    )
    return SummaryResult(source_text=text, summary=response.choices[0].message.content or "")
