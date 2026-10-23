from __future__ import annotations

from typing import Iterable, List
from openai import OpenAI
from database_models import DocumentRecord, SummaryResult


OPENAI_MODEL = "gpt-4o-mini"


def summarize_records(records: Iterable[DocumentRecord]) -> List[SummaryResult]:
    client = OpenAI()
    results: List[SummaryResult] = []
    for record in records:
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": "Summarize the document record in 2 concise sentences."}],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": str(record.content)}],
                },
            ],
        )
        results.append(SummaryResult(id=record.id, summary=response.output_text.strip(), model=OPENAI_MODEL))
    return results
