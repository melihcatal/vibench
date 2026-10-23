from __future__ import annotations

import os
from typing import Dict, List

from anthropic import Anthropic

from document_models import StructuredFieldResult


SYSTEM_PROMPT = "Extract structured business document fields and return strict JSON only."


def extract_document_fields(normalized_text: str, field_names: List[str]) -> StructuredFieldResult:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = {
        "fields": field_names,
        "document_text": normalized_text,
    }
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1200,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Return a JSON object with fields and values: {prompt}"}
        ],
    )
    text_parts = [block.text for block in response.content if getattr(block, "type", "") == "text"]
    raw_text = "".join(text_parts).strip()
    fields: Dict[str, str] = {name: "" for name in field_names}
    return StructuredFieldResult(
        provider="anthropic",
        fields={"raw_json_text": raw_text, **fields},
        raw=response.model_dump(),
    )
