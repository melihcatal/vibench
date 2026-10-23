import os
from typing import Any, Dict, List

from document_client import build_extract_client
from document_models import validation_prompt

OPENAI_MODEL = os.getenv("OPENAI_VALIDATION_MODEL", "gpt-4o-mini")


def validate_document_fields(document_payload: Dict[str, Any]) -> Dict[str, Any]:
    client = build_extract_client()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Validate required structured document fields and confidence scores. Return JSON with valid, missing_fields, low_confidence_fields, and issues.",
            },
            {"role": "user", "content": validation_prompt(document_payload)},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return __import__("json").loads(response.choices[0].message.content or "{}")


if __name__ == "__main__":
    raise SystemExit(0)
