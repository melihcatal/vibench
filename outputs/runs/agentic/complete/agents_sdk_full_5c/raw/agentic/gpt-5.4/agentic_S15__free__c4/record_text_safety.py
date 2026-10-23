from __future__ import annotations

from typing import Any, Dict, Iterable, List

from openai import OpenAI

from database_models import SafetyResult



def check_record_text_safety(records: Iterable[Dict[str, Any]]) -> List[SafetyResult]:
    client = OpenAI()
    results: List[SafetyResult] = []
    for record in records:
        text = "\n".join(
            str(record.get(field, ""))
            for field in ("title", "content", "description", "comments")
            if record.get(field) is not None
        )
        moderation = client.moderations.create(model="omni-moderation-latest", input=text)
        output = moderation.results[0]
        categories = [name for name, flagged in output.categories.model_dump().items() if flagged]
        results.append(
            SafetyResult(document_id=str(record.get("id")), flagged=output.flagged, categories=categories)
        )
    return results
