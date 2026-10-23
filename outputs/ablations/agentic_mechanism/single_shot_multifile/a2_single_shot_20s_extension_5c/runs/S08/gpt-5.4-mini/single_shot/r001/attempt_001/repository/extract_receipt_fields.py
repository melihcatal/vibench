import os
from typing import Any, Dict, Optional

from document_client import build_extract_client, coerce_text_input
from document_models import ExtractRequest, ExtractionResult, normalize_receipt_output

OPENAI_MODEL = os.getenv("OPENAI_RECEIPT_EXTRACTION_MODEL", "gpt-4o-mini")


def extract_receipt_fields(document_text: str, document_id: Optional[str] = None, extra_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = build_extract_client()
    request = ExtractRequest(
        document_type="receipt",
        text=coerce_text_input(document_text),
        document_id=document_id,
        extra_context=extra_context or {},
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Extract structured receipt fields as JSON with merchant, tax, total, and items.",
            },
            {"role": "user", "content": request.to_prompt()},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    payload = response.choices[0].message.content or "{}"
    result = ExtractionResult.from_json(payload)
    return normalize_receipt_output(result.data)


if __name__ == "__main__":
    raise SystemExit(0)
