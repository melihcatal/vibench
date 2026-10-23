# [LATER-STEP] record_summary.py
from typing import List, Dict
from database_models import DocumentRecord


def summarize_records(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate a concise summary for each document returned from a NoSQL query.

    Uses the concrete NoSQL integration indirectly (docs are already raw dicts).
    Returns a new list where each doc is reduced to a lightweight summary dict.
    """
    summaries = []
    for raw in docs:
        record = DocumentRecord(raw)
        # Example summary: id, version, and a few key fields (configurable per use case)
        summary = {
            "id": record.id,
            "version": record.version,
            "type": record.payload.get("type"),
            "title": record.payload.get("title"),
            "created_at": record.payload.get("created_at"),
        }
        summaries.append(summary)
    return summaries
