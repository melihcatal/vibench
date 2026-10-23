from google.cloud import documentai_v1 as documentai
from document_models import InvoiceFields, LineItem
from document_client import (
    GOOGLE_CLOUD_PROJECT_ID,
    GOOGLE_DOCUMENT_AI_LOCATION,
    GOOGLE_DOCUMENT_AI_PROCESSOR_ID,
    validate_google_credentials,
    build_google_document_ai_request_payload,
    parse_google_document_ai_response,
)


def extract_invoice_fields_from_document(
    document_bytes: bytes,
    mime_type: str = "application/pdf",
    processor_id: str = "",
) -> InvoiceFields:
    if not validate_google_credentials():
        raise ValueError(
            "Google Cloud Document AI credentials not configured. "
            "Set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_DOCUMENT_AI_PROCESSOR_ID."
        )

    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(
        GOOGLE_CLOUD_PROJECT_ID,
        GOOGLE_DOCUMENT_AI_LOCATION,
        processor_id or GOOGLE_DOCUMENT_AI_PROCESSOR_ID,
    )

    payload = build_google_document_ai_request_payload(document_bytes, mime_type)
    raw_document = documentai.RawDocument(
        content=payload["raw_document"]["content"].encode("utf-8"),
        mime_type=mime_type,
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    response = client.process_document(request=request)

    parsed = parse_google_document_ai_response(response)
    raw_text = parsed.get("raw_text", "")
    entities = parsed.get("entities", [])

    vendor = _extract_entity_value(entities, "supplier_name") or _extract_entity_value(
        entities, "vendor"
    )
    invoice_date = _extract_entity_value(
        entities, "invoice_date"
    ) or _extract_entity_value(entities, "date")
    total_amount = _extract_entity_float(
        entities, "total_amount"
    ) or _extract_entity_float(entities, "total")
    currency = _extract_entity_value(entities, "currency") or "USD"
    invoice_number = _extract_entity_value(
        entities, "invoice_id"
    ) or _extract_entity_value(entities, "invoice_number")

    line_items = _extract_line_items(entities, raw_text)

    confidence = _calculate_overall_confidence(entities)

    return InvoiceFields(
        vendor=vendor or "Unknown Vendor",
        invoice_date=invoice_date or "",
        total_amount=total_amount or 0.0,
        line_items=line_items,
        currency=currency,
        invoice_number=invoice_number or "",
        confidence=confidence,
        raw_text=raw_text,
    )


def extract_invoice_fields_from_text(
    text_content: str,
    processor_id: str = "",
) -> InvoiceFields:
    document_bytes = text_content.encode("utf-8")
    return extract_invoice_fields_from_document(
        document_bytes, mime_type="text/plain", processor_id=processor_id
    )


def _extract_entity_value(entities: list[dict], entity_type: str) -> str:
    for entity in entities:
        if entity.get("type", "").lower() == entity_type.lower():
            return entity.get("mention_text", "")
    return ""


def _extract_entity_float(entities: list[dict], entity_type: str) -> float:
    value_str = _extract_entity_value(entities, entity_type)
    if value_str:
        cleaned = value_str.replace("$", "").replace(",", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    return 0.0


def _extract_line_items(entities: list[dict], raw_text: str) -> list[LineItem]:
    line_items = []
    item_entities = [e for e in entities if "item" in e.get("type", "").lower()]
    for item_entity in item_entities:
        line_items.append(
            LineItem(
                description=item_entity.get("mention_text", ""),
                quantity=1.0,
                unit_price=0.0,
                total=0.0,
                confidence=item_entity.get("confidence", 0.0),
            )
        )
    return line_items


def _calculate_overall_confidence(entities: list[dict]) -> float:
    if not entities:
        return 0.0
    confidences = [
        e.get("confidence", 0.0) for e in entities if e.get("confidence", 0) > 0
    ]
    if not confidences:
        return 0.0
    return sum(confidences) / len(confidences)
