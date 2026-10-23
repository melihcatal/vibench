import os
from typing import List, Dict, Any, Optional
import re
from datetime import datetime
from google.cloud import documentai
from document_client import get_documentai_client
from document_models import NormalizedDocument, KeyValuePair


def extract_structured_fields(
    normalized_doc: NormalizedDocument, document_type: str = "invoice"
) -> Dict[str, Any]:
    """Extract structured fields from OCR-normalized document text using Google Cloud Document AI."""

    client = get_documentai_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")

    # Use specialized processor based on document type
    processor_id = get_processor_id_for_type(document_type)

    if not normalized_doc.text:
        return {
            "fields": {},
            "document_type": document_type,
            "provider": "google_document_ai",
            "model": f"{document_type}_parser",
            "confidence": 0.0,
        }

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    raw_document = documentai.RawDocument(
        content=normalized_doc.text.encode("utf-8"), mime_type="text/plain"
    )

    request_docai = documentai.ProcessRequest(name=name, raw_document=raw_document)

    try:
        result = client.process_document(request=request_docai)
        document = result.document

        extracted_fields = {}

        if hasattr(document, "entities"):
            for entity in document.entities:
                field_name = entity.type_
                field_value = extract_entity_text(document.text, entity)
                confidence = entity.confidence if hasattr(entity, "confidence") else 0.0

                extracted_fields[field_name] = {
                    "value": field_value,
                    "confidence": confidence,
                    "normalized_value": normalize_field_value(field_name, field_value),
                }

        return {
            "fields": extracted_fields,
            "document_type": document_type,
            "provider": "google_document_ai",
            "model": f"{document_type}_parser",
            "confidence": calculate_average_confidence(extracted_fields),
        }

    except Exception as e:
        # Fallback to rule-based extraction if Document AI fails
        return extract_fields_rule_based(normalized_doc, document_type)


def get_processor_id_for_type(document_type: str) -> str:
    """Get the appropriate Document AI processor ID for the document type."""
    processor_map = {
        "invoice": os.getenv("DOCUMENT_AI_INVOICE_PROCESSOR_ID", "invoice-processor"),
        "receipt": os.getenv("DOCUMENT_AI_RECEIPT_PROCESSOR_ID", "receipt-processor"),
        "form": os.getenv("DOCUMENT_AI_FORM_PROCESSOR_ID", "form-processor"),
        "contract": os.getenv(
            "DOCUMENT_AI_CONTRACT_PROCESSOR_ID", "contract-processor"
        ),
    }
    return processor_map.get(
        document_type, os.getenv("DOCUMENT_AI_PROCESSOR_ID", "general-processor")
    )


def extract_entity_text(full_text: str, entity) -> str:
    """Extract text from an entity in Document AI response."""
    if not hasattr(entity, "text_anchor") or not entity.text_anchor:
        return ""

    text_anchor = entity.text_anchor
    if not text_anchor.text_segments:
        return ""

    text_segment = text_anchor.text_segments[0]
    start_index = text_segment.start_index
    end_index = text_segment.end_index
    return full_text[start_index:end_index]


def normalize_field_value(field_name: str, field_value: str) -> Any:
    """Normalize field value based on field type."""
    if not field_value:
        return None

    field_name_lower = field_name.lower()

    # Date fields
    if any(
        date_keyword in field_name_lower
        for date_keyword in ["date", "issued", "due", "created"]
    ):
        return parse_date(field_value)

    # Amount fields
    if any(
        amount_keyword in field_name_lower
        for amount_keyword in ["amount", "total", "price", "cost", "value"]
    ):
        return parse_currency(field_value)

    # Email fields
    if "email" in field_name_lower:
        return extract_email(field_value)

    # Phone fields
    if any(
        phone_keyword in field_name_lower
        for phone_keyword in ["phone", "mobile", "telephone"]
    ):
        return extract_phone(field_value)

    # Default: return string
    return field_value.strip()


def parse_date(date_str: str) -> Optional[str]:
    """Parse date string into ISO format."""
    try:
        # Try common date formats
        for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d.%m.%Y", "%Y.%m.%d"]:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                return dt.isoformat()
            except ValueError:
                continue
    except:
        pass
    return date_str.strip()


def parse_currency(amount_str: str) -> Optional[float]:
    """Parse currency string into float."""
    try:
        # Remove currency symbols and thousands separators
        cleaned = re.sub(r"[^\d.,-]", "", amount_str)
        cleaned = cleaned.replace(",", "")
        return float(cleaned)
    except:
        return None


def extract_email(text: str) -> Optional[str]:
    """Extract email address from text."""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    phone_pattern = r"[\+]?[1-9][\d]{0,2}[\s]?[\(]?\d{3}[\)]?[\s]?\d{3}[\s]?\d{4}"
    match = re.search(phone_pattern, text)
    return match.group(0) if match else None


def calculate_average_confidence(fields: Dict[str, Any]) -> float:
    """Calculate average confidence across all extracted fields."""
    if not fields:
        return 0.0

    confidences = [
        field["confidence"] for field in fields.values() if "confidence" in field
    ]
    return sum(confidences) / len(confidences) if confidences else 0.0


def extract_fields_rule_based(
    normalized_doc: NormalizedDocument, document_type: str
) -> Dict[str, Any]:
    """Fallback rule-based field extraction."""
    fields = {}

    # Extract from key-value pairs
    for pair in normalized_doc.key_value_pairs:
        key_lower = pair.key.lower()

        # Map common keys to field names
        field_mapping = {
            "invoice": {
                "invoice number": "invoice_number",
                "date": "invoice_date",
                "total": "total_amount",
                "vendor": "vendor_name",
                "customer": "customer_name",
            },
            "receipt": {
                "total": "total_amount",
                "date": "purchase_date",
                "store": "store_name",
                "tax": "tax_amount",
            },
        }

        mapping = field_mapping.get(document_type, {})
        for pattern, field_name in mapping.items():
            if pattern in key_lower:
                fields[field_name] = {
                    "value": pair.value,
                    "confidence": pair.confidence,
                    "normalized_value": normalize_field_value(field_name, pair.value),
                }
                break

    return {
        "fields": fields,
        "document_type": document_type,
        "provider": "rule_based",
        "model": "rule_based_extraction",
        "confidence": calculate_average_confidence(fields),
    }
