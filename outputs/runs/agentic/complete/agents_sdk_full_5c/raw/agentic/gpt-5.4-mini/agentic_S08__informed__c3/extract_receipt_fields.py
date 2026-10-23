from __future__ import annotations

import json
from typing import Any, Dict

from document_client import load_config, invoke_bedrock_text
from document_models import ExtractedDocument, LineItem


def extract_receipt_fields(document_text: str) -> Dict[str, Any]:
    cfg = load_config()
    prompt = (
        "Extract receipt fields as strict JSON with keys merchant, tax, total, currency, items, confidence. "
        "Items should include description, quantity, unit_price, amount. Receipt text follows:\n"
        f"{document_text}"
    )
    raw = invoke_bedrock_text(cfg.receipt_model_id, prompt)
    data = json.loads(raw)
    items = [LineItem(**item) for item in data.get("items", [])]
    doc = ExtractedDocument(
        document_type="receipt",
        merchant=data.get("merchant"),
        tax=data.get("tax"),
        total=data.get("total"),
        currency=data.get("currency"),
        items=items,
        confidence=data.get("confidence"),
        raw=data,
    )
    return {"document": doc, "provider": "amazon.bedrock-runtime", "model_id": cfg.receipt_model_id}
