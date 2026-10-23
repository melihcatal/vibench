from __future__ import annotations

from typing import Iterable, Mapping

from openai import OpenAI

from messaging_models import ProcessingSummary


MODEL_ID = "gpt-4o-mini"


def summarize_processing_results(records: Iterable[Mapping[str, object]]) -> str:
    summary = ProcessingSummary(total=0, succeeded=0, failed=0)
    notes = []
    for record in records:
        summary.total += 1
        status = str(record.get("status", ""))
        if status == "succeeded":
            summary.succeeded += 1
        else:
            summary.failed += 1
        notes.append(f"{record.get('message_id', 'unknown')}: {status}")

    client = OpenAI()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize pub/sub message processing results concisely."},
            {"role": "user", "content": f"Summary stats: total={summary.total}, succeeded={summary.succeeded}, failed={summary.failed}. Details: {'; '.join(notes)}"},
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""
