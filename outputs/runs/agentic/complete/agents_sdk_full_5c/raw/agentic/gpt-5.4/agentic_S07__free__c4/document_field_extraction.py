from __future__ import annotations

import json
import os
from typing import Any, Dict

from openai import OpenAI


MODEL = os.getenv("OPENAI_FIELD_MODEL", "gpt-4o-mini")


def extract_document_fields(normalized_document_text: str, schema_description: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": "Extract structured document fields and return valid JSON only.",
            },
            {
                "role": "user",
                "content": f"Schema:\n{schema_description}\n\nDocument:\n{normalized_document_text}",
            },
        ],
    )
    text = response.output_text
    return json.loads(text)
