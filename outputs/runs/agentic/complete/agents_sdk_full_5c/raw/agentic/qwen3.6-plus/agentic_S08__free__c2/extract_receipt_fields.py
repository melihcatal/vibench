"""Extracts merchant, tax, total, and items from a receipt using Google Document AI."""

import json
import os
from typing import Dict, Any, List, Optional

from google.cloud import documentai_v1 as documentai
from google.api_core import client_options
from google.protobuf import json_format

from document_models import ReceiptExtraction, LineItem, normalize_confidence_score


GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "")
GOOGLE_LOCATION = os.environ.get("GOOGLE_DOCUMENT_AI_LOCATION", "us")
GOOGLE_PROCESSOR_ID = os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID", "")


def extract_receipt_fields(
    document_bytes: bytes,
    project_id: str = GOOGLE_PROJECT_ID,
    location: str = GOOGLE_LOCATION,
    processor_id: str = GOOGLE_PROCESSOR_ID
) -> ReceiptExtraction:
    if not project_id or not processor_id:
        raise ValueError(
            "GOOGLE_PROJECT_ID and GOOGLE_DOCUMENT_AI_PROCESSOR_ID must be set"
        )

    endpoint = f"{location}-documentai.googleapis.com"
    options = client_options.ClientOptions(api_endpoint=endpoint)
    client = documentai.DocumentProcessorServiceClient(client_options=options)

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_bytes,
        mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document
    )

    result = client.process_document(request=request)
    document = result.document

    merchant = _extract_entity_value(document, "supplier_name")
    transaction_date = _extract_entity_value(document, "receipt_date")
    total = _extract_entity_float(document, "total_amount")
    tax = _extract_entity_float(document, "vat_tax")

    items = _extract_receipt_items(document)

    confidence_scores = _collect_confidence_scores(document)
    overall_confidence = (
        sum(confidence_scores) / len(confidence_scores)
        if confidence_scores else 0.0
    )
    overall_confidence = normalize_confidence_score(
        overall_confidence, provider="google_document_ai"
    )

    return ReceiptExtraction(
        merchant=merchant,
        transaction_date=transaction_date,
        total=total or 0.0,
        tax=tax,
        items=items,
        confidence=overall_confidence,
        raw_text=document.text if document else ""
    )


def _extract_entity_value(document, entity_type: str) -> str:
    for entity in document.entities:
        if entity.type_ == entity_type:
            mention = entity.mention_text
            if mention:
                return mention
    return ""


def _extract_entity_float(document, entity_type: str) -> Optional[float]:
    for entity in document.entities:
        if entity.type_ == entity_type:
            mention = entity.mention_text
            try:
                return float(mention.replace("$", "").replace(",", "").strip())
            except (ValueError, TypeError):
                pass
    return None


def _extract_receipt_items(document) -> List[LineItem]:
    items: List[LineItem] = []
    for entity in document.entities:
        if entity.type_ == "line_item":
            description = ""
            quantity = None
            unit_price = None
            item_total = 0.0

            for prop in entity.properties:
                if prop.type_ == "item_description":
                    description = prop.mention_text or ""
                elif prop.type_ == "item_quantity":
                    try:
                        quantity = float(prop.mention_text or "0")
                    except (ValueError, TypeError):
                        pass
                elif prop.type_ == "item_amount":
                    try:
                        unit_price = float((prop.mention_text or "0").replace("$", "").strip())
                    except (ValueError, TypeError):
                        pass
                elif prop.type_ == "item_total":
                    try:
                        item_total = float((prop.mention_text or "0").replace("$", "").strip())
                    except (ValueError, TypeError):
                        pass

            items.append(LineItem(
                description=description,
                quantity=quantity,
                unit_price=unit_price,
                total=item_total
            ))
    return items


def _collect_confidence_scores(document) -> List[float]:
    scores = []
    for entity in document.entities:
        if entity.confidence is not None and entity.confidence > 0:
            scores.append(entity.confidence)
    return scores


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python extract_receipt_fields.py <pdf_or_image_path>")
        sys.exit(1)
    filepath = sys.argv[1]
    with open(filepath, "rb") as f:
        doc_bytes = f.read()
    result = extract_receipt_fields(doc_bytes)
    print(json.dumps(result.model_dump(), indent=2, default=str))
