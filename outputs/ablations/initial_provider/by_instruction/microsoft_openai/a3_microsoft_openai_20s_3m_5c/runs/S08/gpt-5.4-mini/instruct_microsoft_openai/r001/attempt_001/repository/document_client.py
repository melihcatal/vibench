import json
import os
from typing import Any, Dict

from openai import OpenAI

from document_models import DocumentRequest, DocumentResponse, normalize_confidence


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _parse_json(text: str) -> Dict[str, Any]:
    return json.loads(text)


def extract_structured_document(request: DocumentRequest, schema_name: str) -> DocumentResponse:
    client = get_openai_client()
    prompt = f"Extract structured fields for {request.document_type} as JSON with schema {schema_name}. Return only JSON.\n\n{request.document_text}"
    result = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0,
    )
    data = _parse_json(result.output_text)
    fields = data.get("fields", data)
    confidences = {k: normalize_confidence(v) for k, v in data.get("confidences", {}).items()}
    return DocumentResponse(fields=fields, confidences=confidences, raw=data)


def standardize_expense_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": payload.get("vendor") or payload.get("merchant"),
        "date": payload.get("date"),
        "total": payload.get("total"),
        "tax": payload.get("tax"),
        "items": payload.get("items", []),
        "notes": payload.get("notes") or payload.get("memo"),
    }
