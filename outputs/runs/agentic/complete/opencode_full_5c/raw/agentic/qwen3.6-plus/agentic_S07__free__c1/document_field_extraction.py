from __future__ import annotations

import json

from openai import OpenAI

from document_models import FieldExtractionResult
from document_client import OPENAI_API_KEY, OPENAI_API_BASE, FIELD_EXTRACTION_MODEL

OPENAI_CHAT_ENDPOINT = "https://api.openai.com/v1/chat/completions"

DEFAULT_EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {},
    "additionalProperties": False,
}


def extract_fields_from_text(
    text: str,
    field_schema: dict | None = None,
    api_key: str | None = None,
    api_base: str | None = None,
    model: str = FIELD_EXTRACTION_MODEL,
) -> FieldExtractionResult:
    key = api_key or OPENAI_API_KEY
    base = api_base or OPENAI_API_BASE

    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    schema = field_schema or DEFAULT_EXTRACTION_SCHEMA

    system_prompt = (
        "You are a document field extraction assistant. "
        "Extract structured fields from the provided document text. "
        "Return only valid JSON matching the specified schema. "
        "Do not include any additional text or explanations."
    )

    user_prompt = (
        f"Extract the following fields from this document text:\n\n"
        f"Document text:\n{text}\n\n"
        f"Required JSON schema:\n{json.dumps(schema, indent=2)}"
    )

    client = OpenAI(api_key=key, base_url=base)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or "{}"
    try:
        extracted_fields = json.loads(content)
    except json.JSONDecodeError:
        extracted_fields = {}

    return FieldExtractionResult(
        fields=extracted_fields,
        confidence=1.0 if extracted_fields else 0.0,
        raw_response=response.model_dump()
        if hasattr(response, "model_dump")
        else dict(response),
    )


def extract_fields_from_ocr_result(
    ocr_text: str,
    field_schema: dict | None = None,
    api_key: str | None = None,
    api_base: str | None = None,
    model: str = FIELD_EXTRACTION_MODEL,
) -> FieldExtractionResult:
    return extract_fields_from_text(
        text=ocr_text,
        field_schema=field_schema,
        api_key=api_key,
        api_base=api_base,
        model=model,
    )


def extract_fields_batch(
    texts: list[str],
    field_schema: dict | None = None,
    api_key: str | None = None,
    api_base: str | None = None,
    model: str = FIELD_EXTRACTION_MODEL,
) -> list[FieldExtractionResult]:
    results: list[FieldExtractionResult] = []
    for text in texts:
        result = extract_fields_from_text(
            text=text,
            field_schema=field_schema,
            api_key=api_key,
            api_base=api_base,
            model=model,
        )
        results.append(result)
    return results
