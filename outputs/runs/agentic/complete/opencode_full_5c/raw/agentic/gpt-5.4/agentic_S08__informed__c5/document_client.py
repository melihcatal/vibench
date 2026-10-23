from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_document_intelligence_client() -> DocumentIntelligenceClient:
    endpoint = get_required_env("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = get_required_env("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def analyze_prebuilt_document(
    document_bytes: bytes, model_id: str = "prebuilt-invoice"
) -> Any:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(model_id=model_id, body=document_bytes)
    return poller.result()


def _field_content(field: Any) -> Any:
    if field is None:
        return None
    for attr in (
        "value_string",
        "value_currency",
        "value_date",
        "value_number",
        "value_integer",
        "value_phone_number",
        "value_selection_mark",
        "content",
    ):
        if hasattr(field, attr):
            value = getattr(field, attr)
            if value is not None:
                if attr == "value_currency":
                    amount = getattr(value, "amount", None)
                    currency_code = getattr(value, "currency_code", None)
                    return {"amount": amount, "currency_code": currency_code}
                return value
    return getattr(field, "content", None)


def field_value(field: Any) -> Any:
    value = _field_content(field)
    if isinstance(value, dict) and "amount" in value:
        return value.get("amount")
    return value


def field_currency_code(field: Any) -> Optional[str]:
    value = _field_content(field)
    if isinstance(value, dict):
        return value.get("currency_code")
    return None


def field_confidence(field: Any) -> float:
    return float(getattr(field, "confidence", 0.0) or 0.0)


def extract_line_items(doc_field: Any) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    if not doc_field or not getattr(doc_field, "value_array", None):
        return items
    for entry in doc_field.value_array:
        value_object = getattr(entry, "value_object", None) or {}
        description = value_object.get("Description")
        quantity = value_object.get("Quantity")
        unit_price = value_object.get("UnitPrice")
        amount = value_object.get("Amount") or value_object.get("TotalPrice")
        item_confidences = [
            field_confidence(x)
            for x in [description, quantity, unit_price, amount]
            if x is not None
        ]
        items.append(
            {
                "description": field_value(description) or "",
                "quantity": field_value(quantity),
                "unit_price": field_value(unit_price),
                "amount": field_value(amount),
                "confidence": sum(item_confidences) / len(item_confidences)
                if item_confidences
                else 0.0,
            }
        )
    return items


def first_document(result: Any) -> Any:
    documents = getattr(result, "documents", None) or []
    if not documents:
        raise ValueError(
            "No structured documents were returned by Azure Document Intelligence"
        )
    return documents[0]
