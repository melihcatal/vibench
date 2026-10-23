from __future__ import annotations

from typing import Dict, Iterable, List, Optional
from openai import OpenAI
from database_models import DocumentRecord, SafetyResult, extract_text_fields


PROVIDER = "OpenAI Moderations"


def check_record_text_safety(records: Iterable[DocumentRecord], field_names: Optional[List[str]] = None) -> List[SafetyResult]:
    client = OpenAI()
    results: List[SafetyResult] = []
    for record in records:
        text_fields = extract_text_fields(record.content, field_names=field_names)
        joined_text = "\n".join(f"{k}: {v}" for k, v in text_fields.items())
        moderation = client.moderations.create(model="omni-moderation-latest", input=joined_text)
        entry = moderation.results[0]
        category_scores: Dict[str, float] = {}
        if hasattr(entry, "category_scores") and entry.category_scores is not None:
            category_scores = entry.category_scores.model_dump()
        results.append(
            SafetyResult(
                id=record.id,
                flagged=bool(entry.flagged),
                category_scores=category_scores,
            )
        )
    return results
