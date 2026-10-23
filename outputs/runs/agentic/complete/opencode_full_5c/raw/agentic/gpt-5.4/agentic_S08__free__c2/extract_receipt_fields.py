from __future__ import annotations

from typing import Any, Dict, List

from document_client import get_entity_confidence, get_entity_text, process_document
from document_models import (
    DocumentSource,
    ExtractedReceipt,
    make_confidence_value,
    normalize_line_item,
)


RECEIPT_PROCESSOR_HINT = "google_documentai_receipt_parser"


def _group_entities(entities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for entity in entities:
        grouped.setdefault(entity.get("type", "unknown"), []).append(entity)
    return grouped


def extract_receipt_fields(source: DocumentSource) -> ExtractedReceipt:
    response = process_document(source)
    entities = response.get("document", {}).get("entities", [])
    grouped = _group_entities(entities)
    merchant_entity = (
        grouped.get("supplier_name") or grouped.get("merchant_name") or [None]
    )[0]
    tax_entity = (grouped.get("total_tax_amount") or [None])[0]
    total_entity = (grouped.get("total_amount") or [None])[0]
    item_entities = grouped.get("line_item", [])
    items = []
    for item in item_entities:
        properties = {prop.get("type"): prop for prop in item.get("properties", [])}
        items.append(
            normalize_line_item(
                {
                    "description": get_entity_text(
                        properties.get("line_item/description", {})
                    ),
                    "quantity": get_entity_text(
                        properties.get("line_item/quantity", {})
                    ),
                    "unit_price": get_entity_text(
                        properties.get("line_item/unit_price", {})
                    ),
                    "amount": get_entity_text(properties.get("line_item/amount", {})),
                    "confidence": item.get("confidence"),
                }
            )
        )
    return ExtractedReceipt(
        merchant=make_confidence_value(
            get_entity_text(merchant_entity or {}),
            get_entity_confidence(merchant_entity or {}),
        ),
        tax=make_confidence_value(
            get_entity_text(tax_entity or {}), get_entity_confidence(tax_entity or {})
        ),
        total=make_confidence_value(
            get_entity_text(total_entity or {}),
            get_entity_confidence(total_entity or {}),
        ),
        items=items,
        raw_response=response,
    )
