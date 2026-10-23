from __future__ import annotations

from typing import Any, Dict

import requests

from document_models import ExtractedDocument, LineItem, build_normalized_record, normalized_record_to_dict

OPENEXCHANGERATES_APP_ID = __import__("os").getenv("OPENEXCHANGERATES_APP_ID", "")
OPENEXCHANGERATES_URL = "https://openexchangerates.org/api/latest.json"


class ExpenseNormalizer:
    def normalize(self, extracted: Dict[str, Any], target_currency: str = "USD") -> Dict[str, Any]:
        doc = ExtractedDocument(
            document_type=extracted.get("document_type", "expense"),
            vendor=extracted.get("vendor"),
            merchant=extracted.get("merchant"),
            invoice_date=extracted.get("invoice_date"),
            tax=extracted.get("tax"),
            total=extracted.get("total"),
            currency=extracted.get("currency"),
            notes=extracted.get("notes"),
            line_items=[LineItem(**item) for item in extracted.get("line_items", [])],
            raw_fields=extracted.get("raw_fields", {}),
            provider=extracted.get("provider"),
            model=extracted.get("model"),
        )
        record = build_normalized_record(doc)
        normalized = normalized_record_to_dict(record)
        normalized["normalized_by"] = "openexchangerates"
        normalized["target_currency"] = target_currency
        normalized["fx_rate"] = self._fx_rate(doc.currency, target_currency)
        return normalized

    def _fx_rate(self, source_currency: str | None, target_currency: str) -> float | None:
        if not source_currency or source_currency == target_currency:
            return 1.0 if source_currency else None
        if not OPENEXCHANGERATES_APP_ID:
            return None
        response = requests.get(
            OPENEXCHANGERATES_URL,
            params={"app_id": OPENEXCHANGERATES_APP_ID, "base": "USD", "symbols": f"{source_currency},{target_currency}"},
            timeout=30,
        )
        response.raise_for_status()
        rates = response.json().get("rates", {})
        src = rates.get(source_currency)
        tgt = rates.get(target_currency)
        if not src or not tgt:
            return None
        return float(tgt) / float(src)
