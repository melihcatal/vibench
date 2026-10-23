import os
import json
from typing import Dict, Any, Union, Optional
from google.cloud import documentai_v1 as documentai
from google.api_core import client_options
from document_client import get_google_document_ai_config
from document_models import (
    InvoiceExtraction,
    ReceiptExtraction,
    DocumentValidationResult,
    build_expense_schema,
)


GOOGLE_CLOUD_LOCATION = "us"
DOCUMENT_AI_PROCESSOR_TYPE = "invoice"


def validate_document_fields(
    extraction: Union[InvoiceExtraction, ReceiptExtraction],
    confidence_threshold: float = 0.7,
    document_bytes: Optional[bytes] = None,
) -> DocumentValidationResult:
    config = get_google_document_ai_config()
    project_id = config["project_id"]
    location = config.get("location", GOOGLE_CLOUD_LOCATION)
    processor_id = config.get("processor_id", "")

    if isinstance(extraction, InvoiceExtraction):
        required_fields = ["vendor_name", "invoice_date", "total_amount"]
        field_confidence_map = extraction.confidence_scores
        validation_details = _validate_invoice_structure(extraction)
    elif isinstance(extraction, ReceiptExtraction):
        required_fields = ["merchant_name", "receipt_date", "total_amount"]
        field_confidence_map = extraction.confidence_scores
        validation_details = _validate_receipt_structure(extraction)
    else:
        raise TypeError(f"Unsupported extraction type: {type(extraction)}")

    missing_fields = []
    for field_name in required_fields:
        value = getattr(extraction, field_name, None)
        if (
            value is None
            or (isinstance(value, str) and not value.strip())
            or (isinstance(value, (int, float)) and value == 0)
        ):
            missing_fields.append(field_name)

    low_confidence_fields = []
    field_name_mapping = {
        "VendorName": "vendor_name",
        "InvoiceDate": "invoice_date",
        "ReceiptDate": "receipt_date",
        "InvoiceTotal": "total_amount",
        "Total": "total_amount",
        "merchant_name": "merchant_name",
        "receipt_date": "receipt_date",
        "total_amount": "total_amount",
    }

    for raw_field, mapped_field in field_name_mapping.items():
        if raw_field in field_confidence_map:
            confidence = field_confidence_map[raw_field]
            if confidence < confidence_threshold:
                if mapped_field not in low_confidence_fields:
                    low_confidence_fields.append(mapped_field)

    if document_bytes and project_id and processor_id:
        google_validation = _validate_with_google_document_ai(
            document_bytes, project_id, location, processor_id, confidence_threshold
        )
        validation_details["google_document_ai_validation"] = google_validation
        for field, score in google_validation.get("field_confidences", {}).items():
            if score < confidence_threshold and field not in low_confidence_fields:
                low_confidence_fields.append(field)

    is_valid = len(missing_fields) == 0 and len(low_confidence_fields) == 0

    return DocumentValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        confidence_threshold=confidence_threshold,
        validation_details=validation_details,
    )


def _validate_invoice_structure(invoice: InvoiceExtraction) -> Dict[str, Any]:
    details = {
        "has_vendor": bool(invoice.vendor_name),
        "has_date": bool(invoice.invoice_date),
        "has_total": invoice.total_amount > 0,
        "has_line_items": len(invoice.line_items) > 0,
        "line_items_count": len(invoice.line_items),
        "total_matches_line_items": False,
    }

    if invoice.line_items:
        line_items_total = sum(item.total for item in invoice.line_items)
        details["line_items_total"] = line_items_total
        details["total_matches_line_items"] = (
            abs(line_items_total - invoice.total_amount) < 0.01
        )

    return details


def _validate_receipt_structure(receipt: ReceiptExtraction) -> Dict[str, Any]:
    details = {
        "has_merchant": bool(receipt.merchant_name),
        "has_date": bool(receipt.receipt_date),
        "has_total": receipt.total_amount > 0,
        "has_items": len(receipt.items) > 0,
        "items_count": len(receipt.items),
    }
    return details


def _validate_with_google_document_ai(
    document_bytes: bytes,
    project_id: str,
    location: str,
    processor_id: str,
    confidence_threshold: float,
) -> Dict[str, Any]:
    client_options_config = client_options.ClientOptions(
        api_endpoint=f"{location}-documentai.googleapis.com"
    )

    client = documentai.DocumentProcessorServiceClient(
        client_options=client_options_config
    )

    name = client.processor_path(project_id, location, processor_id)

    response = client.process_document(
        request=documentai.ProcessRequest(
            name=name,
            raw_document=documentai.RawDocument(
                content=document_bytes, mime_type="application/pdf"
            ),
        )
    )

    document = response.document
    field_confidences = {}

    for entity in document.entities:
        field_name = entity.type_
        confidence = entity.confidence
        field_confidences[field_name] = confidence

    return {
        "processor_used": f"projects/{project_id}/locations/{location}/processors/{processor_id}",
        "field_confidences": field_confidences,
        "entity_count": len(document.entities),
        "text_extracted": bool(document.text),
    }


if __name__ == "__main__":
    from document_models import InvoiceExtraction

    sample = InvoiceExtraction(
        vendor_name="Test Vendor",
        invoice_date="2024-01-15",
        total_amount=500.0,
        confidence_scores={
            "VendorName": 0.95,
            "InvoiceDate": 0.88,
            "InvoiceTotal": 0.92,
        },
    )
    result = validate_document_fields(sample)
    print(
        json.dumps(
            {
                "is_valid": result.is_valid,
                "missing_fields": result.missing_fields,
                "low_confidence_fields": result.low_confidence_fields,
            },
            indent=2,
        )
    )
