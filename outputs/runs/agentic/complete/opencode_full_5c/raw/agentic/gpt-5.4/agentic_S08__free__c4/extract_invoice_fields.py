from __future__ import annotations

from typing import Any, Dict, List

from document_client import get_google_document_ai_client
from document_models import ExtractionResult


def _entity_value(entity: Dict[str, Any]) -> Any:
    mention = entity.get("mentionText")
    normalized = entity.get("normalizedValue", {})
    if "moneyValue" in normalized:
        units = float(normalized["moneyValue"].get("units", 0) or 0)
        nanos = float(normalized["moneyValue"].get("nanos", 0) or 0) / 1_000_000_000
        return units + nanos
    if "text" in normalized:
        return normalized["text"]
    if "dateValue" in normalized:
        date_value = normalized["dateValue"]
        year = date_value.get("year")
        month = date_value.get("month")
        day = date_value.get("day")
        if year and month and day:
            return f"{year:04d}-{month:02d}-{day:02d}"
    return mention


def extract_invoice_fields(content: bytes, mime_type: str) -> Dict[str, Any]:
    client = get_google_document_ai_client()
    response = client.process_document(content=content, mime_type=mime_type)
    entities = response.get("document", {}).get("entities", [])
    fields: Dict[str, Dict[str, Any]] = {}
    line_items: List[Dict[str, Any]] = []
    for entity in entities:
        entity_type = entity.get("type", "")
        confidence = float(entity.get("confidence", 0.0) or 0.0)
        if entity_type in {"supplier_name", "vendor_name"}:
            fields["vendor"] = {
                "value": _entity_value(entity),
                "confidence": confidence,
            }
        elif entity_type in {"invoice_date", "date"}:
            fields["date"] = {"value": _entity_value(entity), "confidence": confidence}
        elif entity_type in {"total_amount", "total"}:
            fields["total"] = {"value": _entity_value(entity), "confidence": confidence}
        elif entity_type == "line_item":
            item: Dict[str, Any] = {"confidence": confidence}
            for prop in entity.get("properties", []):
                prop_type = prop.get("type")
                if prop_type in {"line_item/description", "description"}:
                    item["description"] = _entity_value(prop)
                elif prop_type in {"line_item/quantity", "quantity"}:
                    item["quantity"] = _entity_value(prop)
                elif prop_type in {"line_item/unit_price", "unit_price"}:
                    item["unit_price"] = _entity_value(prop)
                elif prop_type in {"line_item/amount", "amount"}:
                    item["amount"] = _entity_value(prop)
            line_items.append(item)
    result = ExtractionResult(
        document_type="invoice",
        provider="google_document_ai",
        fields=fields,
        line_items=line_items,
        raw_response=response,
    )
    return result.to_dict()
