import json
from typing import Dict, Any, Optional, List

from document_client import get_openai_client
from document_models import FieldExtractionResponse

OPENAI_MODEL_ID = "gpt-4o-2024-08-06"
OPENAI_EMBEDDING_MODEL_ID = "text-embedding-3-small"


def extract_fields_from_ocr_text(
    text: str,
    field_schema: Dict[str, Any],
    system_prompt: Optional[str] = None,
) -> FieldExtractionResponse:
    client = get_openai_client()

    default_system = (
        "You are a document field extraction assistant. "
        "Extract structured fields from the provided OCR text according to the schema. "
        "Return only valid JSON matching the schema."
    )

    system_message = system_prompt or default_system

    schema_json = json.dumps(field_schema, indent=2)

    user_message = (
        f"Extract the following fields from the OCR text below.\n\n"
        f"Schema:\n{schema_json}\n\n"
        f"OCR Text:\n{text}"
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL_ID,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0.0,
        response_format={"type": "json_object"},
    )

    extracted_json = response.choices[0].message.content
    fields = json.loads(extracted_json)

    confidence = _estimate_confidence(response, fields)

    return FieldExtractionResponse(
        fields=fields,
        confidence=confidence,
        raw_text=text,
    )


def extract_fields_batch(
    texts: List[str],
    field_schema: Dict[str, Any],
    system_prompt: Optional[str] = None,
) -> List[FieldExtractionResponse]:
    results = []
    for text in texts:
        result = extract_fields_from_ocr_text(
            text=text,
            field_schema=field_schema,
            system_prompt=system_prompt,
        )
        results.append(result)
    return results


def _estimate_confidence(response, fields: Dict[str, Any]) -> float:
    finish_reason = response.choices[0].finish_reason
    if finish_reason != "stop":
        return 0.5

    non_empty = sum(1 for v in fields.values() if v is not None and v != "" and v != [])
    total = len(fields)
    if total == 0:
        return 0.0

    return non_empty / total
