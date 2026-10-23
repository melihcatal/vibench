from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from storage_models import SummaryResult

DEFAULT_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_asset_content(extracted_text: str, metadata_text: Optional[str] = None, model: str = DEFAULT_MODEL) -> SummaryResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = extracted_text.strip()
    if metadata_text:
        prompt = f"Metadata:\n{metadata_text.strip()}\n\nContent:\n{prompt}"

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": "Summarize stored asset content into a concise operational summary."},
            {"role": "user", "content": prompt},
        ],
        max_output_tokens=220,
    )
    return SummaryResult(summary=response.output_text.strip(), model=model)
