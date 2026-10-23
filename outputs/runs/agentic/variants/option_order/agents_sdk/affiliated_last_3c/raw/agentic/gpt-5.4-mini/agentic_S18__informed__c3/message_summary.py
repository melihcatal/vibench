from __future__ import annotations

from typing import Iterable, Mapping

from openai import OpenAI

from messaging_models import SummaryResult, ensure_text


MODEL_ID = "gpt-4o-mini"


def message_summary(records: Iterable[Mapping[str, object]]) -> SummaryResult:
    client = OpenAI()
    lines = []
    total = 0
    succeeded = 0
    failed = 0
    for record in records:
        total += 1
        status = ensure_text(record.get("status", ""))
        if status.lower() == "success":
            succeeded += 1
        else:
            failed += 1
        lines.append(ensure_text(record.get("summary", record)))
    prompt = "Summarize these message processing results concisely:\n" + "\n".join(lines)
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
    )
    summary = response.choices[0].message.content or ""
    return SummaryResult(total=total, succeeded=succeeded, failed=failed, summary=summary, provider="openai")
