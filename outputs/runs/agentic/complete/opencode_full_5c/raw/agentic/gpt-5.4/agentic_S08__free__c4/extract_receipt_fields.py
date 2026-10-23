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
    return normalized.get("text") or mention


def extract_receipt_fields(content: bytes, mime_type: str) -> Dict[str, Any]:
    client = get_google_document_ai_client()
    response = client.process_document(content=content, mime_type=mime_type)
    entities = response.get("document", {}).get("entities", [])
    fields: Dict[str, Dict[str, Any]] = {}
    items: List[Dict[str, Any]] = []
    for entity in entities:
        entity_type = entity.get("type", "")
        confidence = float(entity.get("confidence", 0.0) or 0.0)
        if entity_type in {"supplier_name", "merchant_name"}:
            fields["merchant"] = {
                "value": _entity_value(entity),
                "confidence": confidence,
            }
        elif entity_type in {"total_tax_amount", "tax_amount"}:
            fields["tax"] = {"value": _entity_value(entity), "confidence": confidence}
        elif entity_type in {"total_amount", "total"}:
            fields["total"] = {"value": _entity_value(entity), "confidence": confidence}
        elif entity_type == "line_item":
            item: Dict[str, Any] = {"confidence": confidence}
            for prop in entity.get("properties", []):
                prop_type = prop.get("type")
                if prop_type in {"line_item/description", "description"}:
                    item["description"] = _entity_value(prop)
                elif prop_type in {"line_item/amount", "amount"}:
                    item["amount"] = _entity_value(prop)
                elif prop_type in {"line_item/quantity", "quantity"}:
                    item["quantity"] = _entity_value(prop)
            items.append(item)
    result = ExtractionResult(
        document_type="receipt",
        provider="google_document_ai",
        fields=fields,
        line_items=items,
        raw_response=response,
    )
    return result.to_dict()
