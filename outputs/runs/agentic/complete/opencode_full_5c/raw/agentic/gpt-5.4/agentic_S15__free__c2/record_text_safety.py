from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


def record_text_safety(
    documents: Iterable[Dict[str, Any]], fields: List[str]
) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    extracted = []
    for document in documents:
        extracted.append(
            {field: document.get(field) for field in fields if field in document}
        )
    moderation = client.moderations.create(
        model="omni-moderation-latest", input=[str(item) for item in extracted]
    )
    return {
        "model": "omni-moderation-latest",
        "results": [result.model_dump() for result in moderation.results],
    }
