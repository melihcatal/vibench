"""Validates required structured fields and confidence scores using Azure AI Document Intelligence schema validation."""

import os
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from document_models import (
    DocumentValidationResult,
    InvoiceExtraction,
    ReceiptExtraction,
    NormalizedExpense,
    normalize_confidence_score
)


AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "https://default.cognitiveservices.azure.com/"
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

REQUIRED_INVOICE_FIELDS = ["vendor", "invoice_date", "total"]
REQUIRED_RECEIPT_FIELDS = ["merchant", "transaction_date", "total"]
REQUIRED_NORMALIZED_FIELDS = ["entity_name", "document_type", "transaction_date", "total_amount"]

MINIMUM_CONFIDENCE_THRESHOLD = 0.70


def validate_document_fields(
    extraction: Union[InvoiceExtraction, ReceiptExtraction, NormalizedExpense],
    document_type: str = "invoice",
    min_confidence: float = MINIMUM_CONFIDENCE_THRESHOLD,
    azure_endpoint: str = AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
    azure_key: str = AZURE_DOCUMENT_INTELLIGENCE_KEY
) -> DocumentValidationResult:
    missing_fields = _check_missing_fields(extraction, document_type)
    low_confidence_fields = _check_confidence_scores(extraction, min_confidence)
    overall_confidence = _calculate_overall_confidence(extraction)
    overall_confidence = normalize_confidence_score(
        overall_confidence, provider="azure_form_recognizer"
    )

    field_details = _build_field_details(extraction, document_type)
    is_valid = len(missing_fields) == 0 and len(low_confidence_fields) == 0

    errors = []
    if missing_fields:
        errors.append(f"Missing required fields: {', '.join(missing_fields)}")
    if low_confidence_fields:
        errors.append(f"Fields below confidence threshold ({min_confidence}): {', '.join(low_confidence_fields)}")
    if overall_confidence < min_confidence:
        errors.append(f"Overall confidence {overall_confidence:.2f} is below threshold {min_confidence:.2f}")

    result = DocumentValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        overall_confidence=overall_confidence,
        errors=errors,
        field_details=field_details
    )

    return result


def validate_against_azure_schema(
    document_bytes: bytes,
    model_id: str = "prebuilt-invoice",
    azure_endpoint: str = AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
    azure_key: str = AZURE_DOCUMENT_INTELLIGENCE_KEY
) -> Dict[str, Any]:
    """Validate document structure using Azure Form Recognizer prebuilt model."""
    credential = AzureKeyCredential(azure_key)
    client = DocumentAnalysisClient(
        endpoint=azure_endpoint,
        credential=credential
    )

    poller = client.begin_analyze_document(
        model_id=model_id,
        document=document_bytes
    )
    result = poller.result()

    validation = {
        "model_id": model_id,
        "provider": "azure_document_intelligence",
        "pages": len(result.pages),
        "fields_found": {},
        "confidence_scores": {}
    }

    if hasattr(result, 'documents') and result.documents:
        for doc in result.documents:
            for field_name, field in doc.fields.items():
                validation["fields_found"][field_name] = field.value
                if field.confidence is not None:
                    validation["confidence_scores"][field_name] = field.confidence

    return validation


def _check_missing_fields(
    extraction: Union[InvoiceExtraction, ReceiptExtraction, NormalizedExpense],
    document_type: str
) -> List[str]:
    if isinstance(extraction, InvoiceExtraction):
        required = REQUIRED_INVOICE_FIELDS
        data = {
            "vendor": extraction.vendor,
            "invoice_date": extraction.invoice_date,
            "total": extraction.total
        }
    elif isinstance(extraction, ReceiptExtraction):
        required = REQUIRED_RECEIPT_FIELDS
        data = {
            "merchant": extraction.merchant,
            "transaction_date": extraction.transaction_date,
            "total": extraction.total
        }
    elif isinstance(extraction, NormalizedExpense):
        required = REQUIRED_NORMALIZED_FIELDS
        data = {
            "entity_name": extraction.entity_name,
            "document_type": extraction.document_type,
            "transaction_date": extraction.transaction_date,
            "total_amount": extraction.total_amount
        }
    else:
        return ["unknown_extraction_type"]

    missing = []
    for field in required:
        value = data.get(field)
        if value is None or (isinstance(value, str) and value.strip() == "") or (isinstance(value, (int, float)) and value == 0):
            missing.append(field)
    return missing


def _check_confidence_scores(
    extraction: Union[InvoiceExtraction, ReceiptExtraction, NormalizedExpense],
    min_confidence: float
) -> List[str]:
    low_fields = []

    if isinstance(extraction, InvoiceExtraction):
        if extraction.confidence < min_confidence:
            low_fields.append("overall_confidence")
        if extraction.total > 0 and extraction.confidence < min_confidence:
            low_fields.append("total")

    elif isinstance(extraction, ReceiptExtraction):
        if extraction.confidence < min_confidence:
            low_fields.append("overall_confidence")
        if extraction.total > 0 and extraction.confidence < min_confidence:
            low_fields.append("total")

    elif isinstance(extraction, NormalizedExpense):
        meta = extraction.metadata or {}
        orig_conf = meta.get("original_confidence", extraction.confidence if hasattr(extraction, 'confidence') else 1.0)
        if orig_conf < min_confidence:
            low_fields.append("original_confidence")

    return low_fields


def _calculate_overall_confidence(
    extraction: Union[InvoiceExtraction, ReceiptExtraction, NormalizedExpense]
) -> float:
    if isinstance(extraction, InvoiceExtraction):
        return extraction.confidence
    elif isinstance(extraction, ReceiptExtraction):
        return extraction.confidence
    elif isinstance(extraction, NormalizedExpense):
        meta = extraction.metadata or {}
        return meta.get("original_confidence", 0.0)
    return 0.0


def _build_field_details(
    extraction: Union[InvoiceExtraction, ReceiptExtraction, NormalizedExpense],
    document_type: str
) -> Dict[str, Any]:
    details = {}

    if isinstance(extraction, InvoiceExtraction):
        details["vendor"] = {"value": extraction.vendor, "confidence": extraction.confidence}
        details["invoice_date"] = {"value": extraction.invoice_date, "confidence": extraction.confidence}
        details["total"] = {"value": extraction.total, "confidence": extraction.confidence}
        details["line_items_count"] = {"value": len(extraction.line_items), "confidence": extraction.confidence}

    elif isinstance(extraction, ReceiptExtraction):
        details["merchant"] = {"value": extraction.merchant, "confidence": extraction.confidence}
        details["transaction_date"] = {"value": extraction.transaction_date, "confidence": extraction.confidence}
        details["total"] = {"value": extraction.total, "confidence": extraction.confidence}
        details["items_count"] = {"value": len(extraction.items), "confidence": extraction.confidence}

    elif isinstance(extraction, NormalizedExpense):
        details["entity_name"] = {"value": extraction.entity_name}
        details["document_type"] = {"value": extraction.document_type}
        details["transaction_date"] = {"value": extraction.transaction_date}
        details["total_amount"] = {"value": extraction.total_amount}
        details["tax_amount"] = {"value": extraction.tax_amount}
        details["currency"] = {"value": extraction.currency}

    return details


if __name__ == "__main__":
    invoice = InvoiceExtraction(
        vendor="Acme Supplies Inc.",
        invoice_date="2024-11-15",
        total=1250.00,
        confidence=0.95
    )
    result = validate_document_fields(invoice, document_type="invoice")
    print(json.dumps(result.model_dump(), indent=2, default=str))
