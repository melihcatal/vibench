from __future__ import annotations

from openai import OpenAI

from storage_models import SummaryRequest, SummaryResult


MODEL_ID = "gpt-4o-mini"


def summarize_stored_asset(request: SummaryRequest) -> SummaryResult:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize the provided content succinctly."},
            {"role": "user", "content": request.text},
        ],
        temperature=0.2,
    )
    text = completion.choices[0].message.content or ""
    return SummaryResult(summary=text.strip(), raw=completion.model_dump())
