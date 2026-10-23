from __future__ import annotations

"""Receipt field extraction using AWS Textract."""

import os
from typing import Any, Dict, List

from document_client import get_aws_textract_client
from document_models import ExtractionRequest, ExtractionResponse, FieldValue, normalize_confidence

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def _field_from_summary(summary_field: Dict[str, Any]) -> FieldValue:
    return FieldValue(
        name=summary_field.get("Type", {}).get("Text", "unknown").lower(),
        value=summary_field.get("ValueDetection", {}).get("Text", ""),
        confidence=normalize_confidence(summary_field.get("ValueDetection", {}).get("Confidence")),
        raw=summary_field,
    )


def extract_receipt_fields(request: ExtractionRequest) -> ExtractionResponse:
    client = get_aws_textract_client(region_name=AWS_REGION)
    response = client.analyze_expense(Document=request.to_textract_document())

    expense_docs = response.get("ExpenseDocuments", [])
    fields: List[FieldValue] = []
    for expense_doc in expense_docs:
        for field in expense_doc.get("SummaryFields", []):
            if field.get("Type", {}).get("Text") in {"VENDOR_NAME", "TOTAL", "TAX"}:
                fields.append(_field_from_summary(field))
        for group in expense_doc.get("LineItemGroups", []):
            for line in group.get("LineItems", []):
                for item_field in line.get("LineItemExpenseFields", []):
                    if item_field.get("Type", {}).get("Text") == "ITEM":
                        fields.append(_field_from_summary(item_field))

    return ExtractionResponse(
        document_type="receipt",
        provider="aws_textract",
        model_id=f"textract:{AWS_REGION}:analyze_expense",
        fields=fields,
        metadata={"source": request.source_name, "page_count": request.page_count},
    )
