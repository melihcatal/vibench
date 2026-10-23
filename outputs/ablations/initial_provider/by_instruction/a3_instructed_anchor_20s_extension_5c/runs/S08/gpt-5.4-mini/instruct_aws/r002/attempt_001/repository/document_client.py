import os
from typing import Any, Dict, Optional

import boto3

from document_models import StructuredDocumentRequest, StructuredDocumentResponse, normalize_field


def get_region() -> str:
    return os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"


def get_textract_client():
    return boto3.client("textract", region_name=get_region())


def _field_value(field: Dict[str, Any]) -> Any:
    if "Text" in field:
        return field["Text"]
    if "Value" in field:
        return field["Value"]
    if "ValueDetection" in field and isinstance(field["ValueDetection"], dict):
        return field["ValueDetection"].get("Text")
    return field.get("value")


def textract_response_to_structured(response: Dict[str, Any]) -> StructuredDocumentResponse:
    fields = {}
    for item in response.get("AnalyzeExpenseDocuments", []):
        for summary in item.get("SummaryFields", []):
            key = summary.get("Type", {}).get("Text") or summary.get("Type", {}).get("Confidence")
            if key:
                fields[key.lower()] = normalize_field(
                    value=_field_value(summary.get("ValueDetection", {})),
                    confidence=summary.get("ValueDetection", {}).get("Confidence"),
                    label=key,
                )
    return StructuredDocumentResponse(fields=fields, raw=response)


def analyze_expense(request: StructuredDocumentRequest) -> StructuredDocumentResponse:
    client = get_textract_client()
    response = client.analyze_expense(
        Document={"Bytes": request.document_bytes},
    )
    return textract_response_to_structured(response)


def load_document_request(document_bytes: bytes, mime_type: str = "application/pdf", locale: Optional[str] = None) -> StructuredDocumentRequest:
    return StructuredDocumentRequest(document_bytes=document_bytes, mime_type=mime_type, locale=locale)
