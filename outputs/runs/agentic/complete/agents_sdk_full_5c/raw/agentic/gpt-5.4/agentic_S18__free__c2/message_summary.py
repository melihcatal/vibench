from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from messaging_models import ProcessingResult


OPENAI_MODEL = "gpt-4o-mini"


def summarize_results(results: Iterable[ProcessingResult]) -> str:
    client = OpenAI()
    materialized: List[ProcessingResult] = list(results)
    lines = [f"- {r.message_id}: {r.status} ({r.detail})" for r in materialized]
    prompt = "Summarize the following message processing outcomes for an operations dashboard:\n" + "\n".join(lines)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        max_output_tokens=180,
    )
    return response.output_text
