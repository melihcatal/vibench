from __future__ import annotations

from typing import Any, Dict

from database_models import RecordSummary


def summarize_record(record: Dict[str, Any]) -> RecordSummary:
    document_id = str(record.get("document_id", ""))
    title = str(record.get("title", record.get("name", document_id)))
    parts = []
    for key in ("description", "summary", "body", "content"):
        value = record.get(key)
        if value:
            parts.append(str(value))
    summary = " ".join(parts)[:280]
    return RecordSummary(document_id=document_id, title=title, summary=summary)
