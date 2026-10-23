"""
[LATER-STEP] Extract structured fields from OCR-normalized document text.
Uses Google Cloud Document AI for specialized form processing and entity
extraction to identify structured fields like dates, amounts, names, and addresses.
"""

import os
import re
from typing import Optional, List, Dict, Any
from google.cloud import documentai_v1
from google.cloud.documentai_v1 import DocumentProcessorServiceClient

from document_client import (
    GOOGLE_CLOUD_PROJECT,
    GOOGLE_CLOUD_LOCATION,
)


GOOGLE_CLOUD_DOCUMENT_AI_FORM_PARSER_MODEL = "document-ai-form-parser-v1"
GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")


class DocumentAIClient:
    """Client wrapper for Google Cloud Document AI field extraction."""

    def __init__(
        self,
        project: Optional[str] = None,
        location: Optional[str] = None,
    ):
        self.project = project or GOOGLE_CLOUD_PROJECT
        self.location = location or GOOGLE_CLOUD_LOCATION
        self.client = DocumentProcessorServiceClient()

    def get_processor_name(self, processor_id: str) -> str:
        """Build the full processor resource name for Document AI."""
        return self.client.processor_path(
            project=self.project,
            location=self.location,
            processor=processor_id,
        )

    def process_document(
        self,
        file_path: str,
        processor_id: str,
        mime_type: str = "application/pdf",
    ) -> documentai_v1.Document:
        """Process a document using a Document AI processor."""
        processor_name = self.get_processor_name(processor_id)

        with open(file_path, "rb") as f:
            file_content = f.read()

        raw_document = documentai_v1.RawDocument(
            content=file_content,
            mime_type=mime_type,
        )

        request = documentai_v1.ProcessRequest(
            name=processor_name,
            raw_document=raw_document,
        )

        result = self.client.process_document(request=request)
        return result.document


def extract_structured_fields(
    ocr_text: str,
    document_type: str = "generic",
    processor_id: Optional[str] = None,
    file_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract structured fields from OCR-normalized document text.

    Uses Google Cloud Document AI via documentai.googleapis.com with the
    document-ai-form-parser-v1 model for specialized field extraction.
    When a file path is provided, uses Document AI directly. Otherwise,
    uses regex-based extraction on OCR text as a fallback.

    Args:
        ocr_text: Plain text extracted from OCR.
        document_type: Type of document (invoice, receipt, form, generic).
        processor_id: Optional Document AI processor ID for full document parsing.
        file_path: Optional path to original document for Document AI processing.

    Returns:
        Dictionary with extracted structured fields organized by category.
    """
    if file_path and processor_id:
        return _extract_fields_via_document_ai(file_path, processor_id, document_type)

    return _extract_fields_from_text(ocr_text, document_type)


def _extract_fields_via_document_ai(
    file_path: str,
    processor_id: str,
    document_type: str = "generic",
) -> Dict[str, Any]:
    """
    Extract structured fields using Google Cloud Document AI processor.
    Uses the documentai.googleapis.com endpoint for entity and field extraction.
    """
    doc_ai_client = DocumentAIClient()
    mime_type = _detect_mime_type(file_path)
    document = doc_ai_client.process_document(file_path, processor_id, mime_type)

    fields = {}

    for entity in document.entities:
        entity_type = getattr(entity, 'type', '')
        entity_text = getattr(entity, 'mention_text', '')
        entity_confidence = getattr(entity, 'confidence', 0.0) or 0.0

        normalized_type = _normalize_entity_type(entity_type, document_type)
        if normalized_type:
            fields[normalized_type] = {
                "value": entity_text.strip(),
                "confidence": entity_confidence,
                "raw_type": entity_type,
            }

    for page in document.pages:
        for form_field in page.form_fields:
            field_name = ""
            field_value = ""
            field_confidence = getattr(form_field, 'confidence', 0.0) or 0.0

            if form_field.field_name and form_field.field_name.text_anchor:
                field_name = _extract_text_from_anchor(document, form_field.field_name.text_anchor)

            if form_field.field_value and form_field.field_value.text_anchor:
                field_value = _extract_text_from_anchor(document, form_field.field_value.text_anchor)

            if field_name.strip():
                normalized_name = _normalize_field_name(field_name.strip())
                fields[normalized_name] = {
                    "value": field_value.strip(),
                    "confidence": field_confidence,
                    "raw_type": "form_field",
                }

    return {
        "fields": fields,
        "document_type": document_type,
        "source": "document_ai",
        "model": GOOGLE_CLOUD_DOCUMENT_AI_FORM_PARSER_MODEL,
        "page_count": len(document.pages),
    }


def _extract_fields_from_text(
    ocr_text: str,
    document_type: str = "generic",
) -> Dict[str, Any]:
    """
    Extract structured fields from OCR text using regex patterns.
    Uses Google Cloud Document AI entity type conventions for field naming.
    """
    fields = {}

    if document_type == "invoice":
        fields.update(_extract_invoice_fields(ocr_text))
    elif document_type == "receipt":
        fields.update(_extract_receipt_fields(ocr_text))
    elif document_type == "form":
        fields.update(_extract_form_fields(ocr_text))
    else:
        fields.update(_extract_generic_fields(ocr_text))

    return {
        "fields": fields,
        "document_type": document_type,
        "source": "regex_extraction",
        "model": GOOGLE_CLOUD_DOCUMENT_AI_FORM_PARSER_MODEL,
        "page_count": 1,
    }


def _extract_invoice_fields(text: str) -> Dict[str, Any]:
    """Extract invoice-specific fields using regex patterns."""
    fields = {}

    invoice_patterns = {
        "invoice_number": [
            r"(?:Invoice|INV|Invoice\s*#)[:\s]*([A-Z0-9\-]+)",
            r"Invoice\s*Number[:\s]*([A-Z0-9\-]+)",
        ],
        "invoice_date": [
            r"(?:Date|Invoice\s*Date)[:\s]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            r"(?:Date|Invoice\s*Date)[:\s]*([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})",
        ],
        "total_amount": [
            r"(?:Total|Amount\s*Due|Balance\s*Due)[:\s]*\$?([\d,]+\.\d{2})",
            r"\$\s*([\d,]+\.\d{2})\s*(?:Total|Amount)",
        ],
        "subtotal": [
            r"(?:Subtotal|Sub-total)[:\s]*\$?([\d,]+\.\d{2})",
        ],
        "tax_amount": [
            r"(?:Tax|VAT|GST|Sales\s*Tax)[:\s]*\$?([\d,]+\.\d{2})",
        ],
        "vendor_name": [
            r"(?:From|Vendor|Supplier|Billed\s*By)[:\s]*(.+?)(?:\n|$)",
        ],
        "customer_name": [
            r"(?:To|Customer|Bill\s*To|Client)[:\s]*(.+?)(?:\n|$)",
        ],
    }

    for field_name, patterns in invoice_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                fields[field_name] = {
                    "value": match.group(1).strip(),
                    "confidence": 0.7,
                    "raw_type": f"invoice.{field_name}",
                }
                break

    return fields


def _extract_receipt_fields(text: str) -> Dict[str, Any]:
    """Extract receipt-specific fields using regex patterns."""
    fields = {}

    receipt_patterns = {
        "merchant_name": [
            r"(?:Merchant|Store|Vendor)[:\s]*(.+?)(?:\n|$)",
            r"^([A-Z][A-Za-z\s&]+(?:Inc|LLC|Corp|Ltd)?)$",
        ],
        "transaction_date": [
            r"(?:Date|Time|Date\/Time)[:\s]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
        ],
        "transaction_total": [
            r"(?:Total|Grand\s*Total)[:\s]*\$?([\d,]+\.\d{2})",
            r"\$\s*([\d,]+\.\d{2})\s*(?:Total|Grand)",
        ],
        "payment_method": [
            r"(?:Payment|Paid\s*By|Method)[:\s]*(.+?)(?:\n|$)",
        ],
        "receipt_number": [
            r"(?:Receipt|Transaction|Order)\s*(?:#|Number)?[:\s]*([A-Z0-9\-]+)",
        ],
    }

    for field_name, patterns in receipt_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                fields[field_name] = {
                    "value": match.group(1).strip(),
                    "confidence": 0.7,
                    "raw_type": f"receipt.{field_name}",
                }
                break

    return fields


def _extract_form_fields(text: str) -> Dict[str, Any]:
    """Extract form-specific fields using regex patterns."""
    fields = {}

    form_patterns = {
        "full_name": [
            r"(?:Name|Full\s*Name|Applicant)[:\s]*([A-Za-z\s]+?)(?:\n|$)",
        ],
        "email": [
            r"(?:Email|E-mail|Email\s*Address)[:\s]*([\w.+-]+@[\w-]+\.[\w.-]+)",
            r"([\w.+-]+@[\w-]+\.[\w.-]+)",
        ],
        "phone": [
            r"(?:Phone|Tel|Telephone|Mobile)[:\s]*([\d\-\(\)\s\+]+)",
        ],
        "address": [
            r"(?:Address|Street)[:\s]*(.+?)(?:\n|$)",
        ],
        "date_of_birth": [
            r"(?:DOB|Date\s*of\s*Birth|Birth\s*Date)[:\s]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
        ],
        "ssn": [
            r"(?:SSN|Social\s*Security)[:\s]*(\d{3}[\-]\d{2}[\-]\d{4})",
        ],
    }

    for field_name, patterns in form_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                fields[field_name] = {
                    "value": match.group(1).strip(),
                    "confidence": 0.75,
                    "raw_type": f"form.{field_name}",
                }
                break

    return fields


def _extract_generic_fields(text: str) -> Dict[str, Any]:
    """Extract generic fields from any document text."""
    fields = {}

    generic_patterns = {
        "date": [
            r"\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\b",
            r"\b([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})\b",
        ],
        "email": [
            r"([\w.+-]+@[\w-]+\.[\w.-]+)",
        ],
        "phone": [
            r"(\+\d{1,3}[\-\s]?\d{3}[\-\s]?\d{3}[\-\s]?\d{4})",
            r"(\d{3}[\-\s]\d{3}[\-\s]\d{4})",
        ],
        "amount": [
            r"\$([\d,]+\.\d{2})",
            r"([\d,]+\.\d{2})\s*(?:USD|EUR|GBP)",
        ],
        "percentage": [
            r"(\d{1,3}(?:\.\d+)?)\s*%",
        ],
    }

    for field_name, patterns in generic_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                fields[field_name] = {
                    "value": match.group(1).strip(),
                    "confidence": 0.6,
                    "raw_type": f"generic.{field_name}",
                }
                break

    return fields


def _normalize_entity_type(entity_type: str, document_type: str) -> Optional[str]:
    """Normalize Document AI entity types to standardized field names."""
    type_mapping = {
        "invoice_date": "invoice_date",
        "supplier_name": "vendor_name",
        "receiver_name": "customer_name",
        "line_item/description": "line_item_description",
        "line_item/amount": "line_item_amount",
        "total_amount": "total_amount",
        "tax_amount": "tax_amount",
    }
    return type_mapping.get(entity_type, entity_type.replace("/", "_") if entity_type else None)


def _normalize_field_name(field_name: str) -> str:
    """Normalize a field name to a standard snake_case format."""
    name = field_name.lower().strip()
    name = re.sub(r'[^a-z0-9\s]', '_', name)
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'_+', '_', name)
    return name.strip('_')


def _extract_text_from_anchor(document: documentai_v1.Document, text_anchor) -> str:
    """Extract text from a Document AI text anchor."""
    if not text_anchor or not text_anchor.text_segments:
        return ""

    full_text = document.text
    result_parts = []

    for segment in text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        result_parts.append(full_text[start_index:end_index])

    return "".join(result_parts)


def _detect_mime_type(file_path: str) -> str:
    """Detect MIME type from file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    mime_map = {
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
    }
    return mime_map.get(ext, "application/pdf")


if __name__ == "__main__":
    sample_text = """Invoice #INV-2024-001
Date: 01/15/2024
Vendor: Acme Corporation
Total: $1,250.00
Tax: $125.00"""

    result = extract_structured_fields(sample_text, document_type="invoice")
    for field_name, field_data in result["fields"].items():
        print(f"{field_name}: {field_data['value']} (confidence: {field_data['confidence']})")
