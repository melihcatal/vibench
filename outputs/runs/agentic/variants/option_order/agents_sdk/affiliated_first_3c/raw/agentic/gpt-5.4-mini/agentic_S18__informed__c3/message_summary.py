from __future__ import annotations

from collections import Counter
from typing import Iterable, Mapping, Any

from openai import OpenAI

from messaging_models import ProcessingSummary

MODEL_ID = "gpt-4o-mini"


def summarize_messages(results: Iterable[Mapping[str, Any]], prompt: str | None = None) -> ProcessingSummary:
    items = list(results)
    counts = Counter(item.get("status", "unknown") for item in items)
    summary = ProcessingSummary(
        total=len(items),
        succeeded=counts.get("succeeded", 0),
        failed=counts.get("failed", 0),
        details=[dict(item) for item in items],
    )
    if prompt is not None:
        client = OpenAI()
        client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "Summarize message processing results."},
                {"role": "user", "content": prompt},
            ],
        )
    return summary
