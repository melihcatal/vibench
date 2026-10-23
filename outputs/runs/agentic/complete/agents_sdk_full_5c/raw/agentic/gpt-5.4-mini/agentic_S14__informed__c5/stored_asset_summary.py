from __future__ import annotations

import os

from openai import OpenAI

from storage_models import SummaryRequest, SummaryResult, normalize_text


OPENAI_MODEL_ENV = "OPENAI_SUMMARY_MODEL"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"


def summarize_stored_asset(text: str, max_output_tokens: int = 256) -> SummaryResult:
    request = SummaryRequest(text=text, max_output_tokens=max_output_tokens)
    client = OpenAI()
    model = os.getenv(OPENAI_MODEL_ENV, DEFAULT_OPENAI_MODEL)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize the provided document content clearly and concisely."},
            {"role": "user", "content": normalize_text(request.text)},
        ],
        max_tokens=request.max_output_tokens,
    )
    summary = response.choices[0].message.content if response.choices else ""
    return SummaryResult(summary=summary or "", raw=response)
