from __future__ import annotations

from typing import Any, Dict, List

from database_models import DocumentRecord, as_iso_utc


AZURE_OPENAI_MODEL = "gpt-4o-mini"


def summarize_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(records)
    titles = [str(r.get("title", r.get("id", ""))) for r in records[:5]]
    return {
        "model": AZURE_OPENAI_MODEL,
        "total_records": total,
        "sample_titles": titles,
        "generated_at": as_iso_utc(),
    }
