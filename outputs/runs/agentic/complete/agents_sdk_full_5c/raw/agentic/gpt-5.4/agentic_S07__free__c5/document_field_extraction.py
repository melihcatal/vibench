from __future__ import annotations

import json
import os
from typing import Any, Dict

from openai import OpenAI


PROVIDER = "openai"
MODEL = "gpt-4.1-mini"


def document_field_extraction(normalized_text: str, schema: Dict[str, str]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = {
        "schema": schema,
        "document_text": normalized_text,
    }
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": "Extract structured fields from OCR-normalized document text. Return only valid JSON."},
            {"role": "user", "content": json.dumps(prompt)},
        ],
    )
    return json.loads(response.output_text)
