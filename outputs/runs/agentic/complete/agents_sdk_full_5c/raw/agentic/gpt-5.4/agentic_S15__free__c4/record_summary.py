from __future__ import annotations

from typing import Any, Dict, Iterable, List

from openai import OpenAI

from database_models import RecordSummary


OPENAI_MODEL = "gpt-4o-mini"



def summarize_records(records: Iterable[Dict[str, Any]]) -> List[RecordSummary]:
    client = OpenAI()
    summaries: List[RecordSummary] = []
    for record in records:
        title = str(record.get("title") or record.get("name") or record.get("id"))
        body = str(record.get("content") or record.get("description") or record)
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=f"Summarize this document in 1-2 sentences. Title: {title}\nContent: {body}",
        )
        summaries.append(
            RecordSummary(
                document_id=str(record.get("id")),
                title=title,
                summary=response.output_text.strip(),
                source_language=record.get("language"),
            )
        )
    return summaries
