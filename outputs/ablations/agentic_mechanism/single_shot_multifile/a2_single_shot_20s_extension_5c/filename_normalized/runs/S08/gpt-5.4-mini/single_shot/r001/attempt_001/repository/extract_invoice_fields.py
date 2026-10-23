import os
from typing import Any, Dict, Optional
import requests

from document_client import build_extract_client, coerce_text_input
from document_models import ExtractRequest, ExtractionResult, normalize_invoice_output

OPENAI_MODEL = os.getenv("OPENAI_INVOICE_EXTRACTION_MODEL", "gpt-4o-mini")


def extract_invoice_fields(document_text: str, document_id: Optional[str] = None, extra_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = build_extract_client()
    request = ExtractRequest(
        document_type="invoice",
        text=coerce_text_input(document_text),
        document_id=document_id,
        extra_context=extra_context or {},
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Extract structured invoice fields as JSON with vendor, date, total, and line_items.",
            },
            {"role": "user", "content": request.to_prompt()},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    payload = response.choices[0].message.content or "{}"
    result = ExtractionResult.from_json(payload)
    return normalize_invoice_output(result.data)


if __name__ == "__main__":
    raise SystemExit(0)
