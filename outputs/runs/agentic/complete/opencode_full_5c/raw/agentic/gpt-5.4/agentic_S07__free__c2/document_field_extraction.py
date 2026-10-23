from __future__ import annotations

import json
from typing import Any, Dict

from document_client import get_default_extraction_model, get_openai_client


def extract_document_fields(text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    client = get_openai_client()
    response = client.responses.create(
        model=get_default_extraction_model(),
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract structured fields from OCR-normalized document text and return only JSON matching the provided schema.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Schema:\n{json.dumps(schema)}\n\nDocument text:\n{text}",
                    }
                ],
            },
        ],
        text={"format": {"type": "json_object"}},
    )
    return json.loads(response.output_text)
