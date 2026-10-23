"""Summarize retrieved document records using OpenAI GPT-4o.

Provider: OpenAI / Azure OpenAI chat completions (openai SDK)
Auth env: OPENAI_API_KEY
Model: gpt-4o
"""

from __future__ import annotations

import os
import json
from typing import Any, Dict, List, Optional

from openai import OpenAI

from database_models import DocumentResponse


_OPENAI_MODEL = "gpt-4o"


def _build_messages(records: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    system_prompt = (
        "You are a document analyst. Summarize the following set of database "
        "records into a concise paragraph highlighting key entities, statuses, "
        "and notable fields. Keep the summary under 150 words."
    )
    user_content = json.dumps(records, indent=2, default=str)
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]


def summarize_records(
    records: List[DocumentResponse],
    model: Optional[str] = None,
) -> str:
    """Use OpenAI GPT-4o to generate a summary of the given document records."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = model or _OPENAI_MODEL

    record_dicts = [
        {"id": r.doc_id, "version": r.version, "data": r.data}
        for r in records
    ]

    messages = _build_messages(record_dicts)
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.3,
        max_tokens=300,
    )

    summary = response.choices[0].message.content
    return summary or ""


if __name__ == "__main__":
    sample = [
        DocumentResponse(doc_id="doc-1", data={"title": "Report A", "status": "active"}, version=1, found=True),
        DocumentResponse(doc_id="doc-2", data={"title": "Report B", "status": "draft"}, version=2, found=True),
    ]
    print(summarize_records(sample))
