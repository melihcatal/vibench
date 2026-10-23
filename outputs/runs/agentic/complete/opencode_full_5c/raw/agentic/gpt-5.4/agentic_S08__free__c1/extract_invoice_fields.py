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


INVOICE_PROCESSOR_HINT = "google-documentai-invoice-parser"


def extract_invoice_fields(
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
        "vendor": _extract_entity(entities, ["supplier_name", "vendor_name"]),
        "date": _extract_entity(entities, ["invoice_date", "date"]),
        "total": _extract_entity(entities, ["total_amount", "invoice_total"]),
    }
    line_items = _extract_line_items(entities)
    result = ExtractionResult(
        document_type="invoice",
        provider="google_document_ai",
        fields=fields,
        line_items=line_items,
        raw_response=document,
    )
    return result.to_dict()


def _extract_entity(
    entities: List[Dict[str, Any]], type_names: List[str]
) -> ExtractedField:
    for entity in entities:
        if entity.get("type") in type_names:
            mention_text = entity.get("mention_text")
            normalized = entity.get("normalized_value", {})
            normalized_value = normalized.get("text") or normalized.get(
                "money_value", {}
            ).get("units")
            return ExtractedField(
                name=entity.get("type", type_names[0]),
                value=mention_text,
                confidence=normalize_confidence(entity.get("confidence")),
                normalized_value=normalized_value,
            )
    return ExtractedField(
        name=type_names[0], value=None, confidence=0.0, normalized_value=None
    )


def _extract_line_items(entities: List[Dict[str, Any]]) -> List[LineItem]:
    items: List[LineItem] = []
    for entity in entities:
        if entity.get("type") != "line_item":
            continue
        props = {prop.get("type"): prop for prop in entity.get("properties", [])}
        items.append(
            LineItem(
                description=props.get("line_item/description", {}).get("mention_text"),
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
