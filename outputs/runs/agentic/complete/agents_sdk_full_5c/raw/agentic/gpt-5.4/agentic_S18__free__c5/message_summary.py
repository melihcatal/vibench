from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from messaging_models import ProcessingResult


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_results(results: Iterable[ProcessingResult]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    lines: List[str] = []
    for result in results:
        lines.append(f"message_id={result.message_id} status={result.status} details={result.details}")
    prompt = "Summarize the pub/sub message processing results in concise operational language:\n" + "\n".join(lines)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    return response.output_text.strip()
