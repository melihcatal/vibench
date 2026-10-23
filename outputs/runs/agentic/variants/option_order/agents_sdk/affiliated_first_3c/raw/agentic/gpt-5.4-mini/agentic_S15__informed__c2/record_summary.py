from typing import Iterable, Mapping

from openai import OpenAI

from database_models import SummaryResponse

MODEL_ID = "gpt-4o-mini"


def summarize_records(records: Iterable[Mapping[str, object]]) -> SummaryResponse:
    client = OpenAI()
    payload = [dict(record) for record in records]
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize retrieved document records concisely."},
            {"role": "user", "content": str(payload)},
        ],
    )
    summary = response.choices[0].message.content or ""
    return SummaryResponse(summary=summary, document_count=len(payload))
