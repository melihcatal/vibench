"""Extract merchant, tax, total, and items from a receipt using Google Cloud Document AI."""

import os
from google.cloud import documentai_v1
from google.api_core import exceptions as google_exceptions
from document_models import ReceiptExtractionRequest, ReceiptExtractionResponse, ReceiptItem


def extract_receipt_fields(request: ReceiptExtractionRequest) -> ReceiptExtractionResponse:
    """Extract structured fields from receipt document using Google Cloud Document AI."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID", "")
    processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    client = documentai_v1.DocumentProcessorServiceClient()

    with open(request.document_path, "rb") as f:
        document_bytes = f.read()

    raw_document = documentai_v1.RawDocument(
        content=document_bytes,
        mime_type="application/pdf",
    )

    online_process_request = documentai_v1.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    try:
        result = client.process_document(request=online_process_request)
    except google_exceptions.GoogleAPIError as exc:
        raise RuntimeError(f"Google Cloud Document AI processing failed: {exc}") from exc

    document = result.document
    entities = document.entities

    merchant = _extract_entity_value(entities, "supplier_name")
    tax = _extract_entity_value(entities, "tax")
    total = _extract_entity_entity_value(entities, "total_amount")
    subtotal = _extract_entity_value(entities, "subtotal")
    date = _extract_entity_value(entities, "purchase_date")

    items = _extract_receipt_items(entities)

    confidence = document.text_extraction_confidence if document.text_extraction_confidence else 0.0

    return ReceiptExtractionResponse(
        merchant=merchant,
        tax_amount=tax,
        total_amount=total,
        subtotal=subtotal,
        receipt_date=date,
        items=items,
        confidence=confidence,
        provider="google_document_ai",
    )


def _extract_entity_value(entities, type_name: str) -> str:
    """Extract entity value by type from Document AI response entities."""
    for entity in entities:
        if entity.type_.lower() == type_name.lower():
            return entity.mention_text or ""
    return ""


def _extract_entity_entity_value(entities, type_name: str) -> str:
    """Extract entity value by type from Document AI response entities."""
    for entity in entities:
        if entity.type_.lower() == type_name.lower():
            return entity.mention_text or ""
    return ""


def _extract_receipt_items(entities) -> list[ReceiptItem]:
    """Extract line items from Document AI receipt entities."""
    items = []
    for entity in entities:
        if entity.type_.lower() in ("line_item", "item", "product"):
            description = entity.mention_text or ""
            quantity = ""
            price = ""

            for prop in entity.properties:
                if prop.type_.lower() in ("quantity", "qty"):
                    quantity = prop.mention_text or ""
                elif prop.type_.lower() in ("price", "amount", "total"):
                    price = prop.mention_text or ""

            items.append(
                ReceiptItem(
                    description=description,
                    quantity=quantity,
                    price=price,
                )
            )

    return items


if __name__ == "__main__":
    req = ReceiptExtractionRequest(document_path="sample_receipt.pdf")
    result = extract_receipt_fields(req)
    print(result)
