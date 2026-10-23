from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from messaging_models import ProcessingResult


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini")


def summarize_processing_results(
    results: list[dict[str, Any] | ProcessingResult],
) -> dict[str, str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    normalized = []
    for result in results:
        if isinstance(result, ProcessingResult):
            normalized.append(result.__dict__)
        else:
            normalized.append(dict(result))
    prompt = {
        "task": "Summarize message processing outcomes for operators",
        "results": normalized,
    }
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You summarize processing results into concise operational text.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    summary = response.output_text.strip()
    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "summary": summary,
    }
