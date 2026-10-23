from __future__ import annotations

from typing import Any, Dict, List, Optional

from document_client import process_document
from document_models import (
    DocumentSource,
    ExtractedField,
    ExtractionResult,
    LineItem,
    normalize_confidence,
)


RECEIPT_PROCESSOR_HINT = "google-documentai-expense-parser"


def extract_receipt_fields(
    content_base64: Optional[str] = None,
    mime_type: str = "application/pdf",
    gcs_uri: Optional[str] = None,
) -> Dict[str, Any]:
    source = DocumentSource(
        content_base64=content_base64, mime_type=mime_type, gcs_uri=gcs_uri
    )
    document = process_document(source)
    entities = document.get("entities", [])
    fields: Dict[str, ExtractedField] = {
        "merchant": _extract_entity(entities, ["supplier_name", "merchant_name"]),
        "tax": _extract_entity(entities, ["total_tax_amount", "tax_amount"]),
        "total": _extract_entity(entities, ["total_amount", "receipt_total"]),
    }
    items = _extract_line_items(entities)
    result = ExtractionResult(
        document_type="receipt",
        provider="google_document_ai",
        fields=fields,
        line_items=items,
        raw_response=document,
    )
    return result.to_dict()


def _extract_entity(
    entities: List[Dict[str, Any]], type_names: List[str]
) -> ExtractedField:
    for entity in entities:
        if entity.get("type") in type_names:
            normalized = entity.get("normalized_value", {})
            normalized_value = normalized.get("text") or normalized.get(
                "money_value", {}
            ).get("units")
            return ExtractedField(
                name=entity.get("type", type_names[0]),
                value=entity.get("mention_text"),
                confidence=normalize_confidence(entity.get("confidence")),
                normalized_value=normalized_value,
            )
    return ExtractedField(
        name=type_names[0], value=None, confidence=0.0, normalized_value=None
    )


def _extract_line_items(entities: List[Dict[str, Any]]) -> List[LineItem]:
    items: List[LineItem] = []
    for entity in entities:
        if entity.get("type") not in {"line_item", "receipt_item"}:
            continue
        props = {prop.get("type"): prop for prop in entity.get("properties", [])}
        items.append(
            LineItem(
                description=props.get("line_item/description", {}).get("mention_text")
                or props.get("receipt_item/description", {}).get("mention_text"),
                quantity=_to_float(
                    props.get("line_item/quantity", {}).get("mention_text")
                ),
                unit_price=_to_float(
                    props.get("line_item/unit_price", {}).get("mention_text")
                ),
                amount=_to_float(props.get("line_item/amount", {}).get("mention_text")),
                confidence=normalize_confidence(entity.get("confidence")),
            )
        )
    return items


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(str(value).replace(",", "").replace("$", "").strip())
    except ValueError:
        return None
