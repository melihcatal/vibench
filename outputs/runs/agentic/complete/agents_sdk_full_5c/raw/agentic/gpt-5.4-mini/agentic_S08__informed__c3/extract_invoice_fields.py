from __future__ import annotations

import json
from typing import Any, Dict

from document_client import load_config, invoke_bedrock_text
from document_models import ExtractedDocument, LineItem


def extract_invoice_fields(document_text: str) -> Dict[str, Any]:
    cfg = load_config()
    prompt = (
        "Extract invoice fields as strict JSON with keys vendor, date, total, currency, notes, items, confidence. "
        "Each item should include description, quantity, unit_price, amount. Invoice text follows:\n"
        f"{document_text}"
    )
    raw = invoke_bedrock_text(cfg.invoice_model_id, prompt)
    data = json.loads(raw)
    items = [LineItem(**item) for item in data.get("items", [])]
    doc = ExtractedDocument(
        document_type="invoice",
        vendor=data.get("vendor"),
        date=data.get("date"),
        total=data.get("total"),
        currency=data.get("currency"),
        notes=data.get("notes"),
        items=items,
        confidence=data.get("confidence"),
        raw=data,
    )
    return {"document": doc, "provider": "amazon.bedrock-runtime", "model_id": cfg.invoice_model_id}
