from __future__ import annotations

from collections import Counter
from typing import Iterable

from openai import OpenAI

from messaging_models import MessageSummary

MODEL = "gpt-4o-mini"


def summarize_message_processing(results: Iterable[dict]) -> dict:
    rows = list(results)
    stats = Counter(row.get("status", "unknown") for row in rows)
    summary = MessageSummary(
        total=len(rows),
        succeeded=stats.get("succeeded", 0),
        failed=stats.get("failed", 0),
        details=rows,
    )
    client = OpenAI()
    client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Summarize message processing outcomes concisely."},
            {"role": "user", "content": f"{summary.total} total, {summary.succeeded} succeeded, {summary.failed} failed."},
        ],
    )
    return summary.__dict__
