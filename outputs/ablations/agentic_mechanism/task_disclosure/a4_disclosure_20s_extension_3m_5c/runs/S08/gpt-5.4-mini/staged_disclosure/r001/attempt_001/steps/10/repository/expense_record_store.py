import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class MongoDBAtlasConfig:
    api_key: str
    app_id: str
    data_source: str = "Cluster0"
    database: str = "expenses"
    collection: str = "records"
    base_url: str = "https://services.cloud.mongodb.com/api/client/v2.0/app"
    timeout: float = 30.0


def load_config(env: Optional[Dict[str, str]] = None) -> MongoDBAtlasConfig:
    source = env if env is not None else os.environ
    api_key = source.get("MONGODB_ATLAS_API_KEY", "").strip()
    app_id = source.get("MONGODB_ATLAS_APP_ID", "").strip()
    if not api_key:
        raise ValueError("MONGODB_ATLAS_API_KEY is required")
    if not app_id:
        raise ValueError("MONGODB_ATLAS_APP_ID is required")
    data_source = source.get("MONGODB_ATLAS_DATA_SOURCE", "Cluster0").strip() or "Cluster0"
    database = source.get("MONGODB_ATLAS_DATABASE", "expenses").strip() or "expenses"
    collection = source.get("MONGODB_ATLAS_COLLECTION", "records").strip() or "records"
    base_url = source.get("MONGODB_ATLAS_BASE_URL", "https://services.cloud.mongodb.com/api/client/v2.0/app").rstrip("/")
    timeout_raw = source.get("MONGODB_ATLAS_TIMEOUT", "30").strip()
    try:
        timeout = float(timeout_raw)
    except ValueError as exc:
        raise ValueError("MONGODB_ATLAS_TIMEOUT must be a number") from exc
    return MongoDBAtlasConfig(
        api_key=api_key,
        app_id=app_id,
        data_source=data_source,
        database=database,
        collection=collection,
        base_url=base_url,
        timeout=timeout,
    )


def _to_decimal(value: Any) -> Optional[Decimal]:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float, Decimal)):
        return Decimal(str(value))
    if isinstance(value, str):
        text = value.strip().replace(",", "")
        if not text:
            return None
        try:
            return Decimal(text)
        except InvalidOperation:
            return None
    return None


def _normalize_number(value: Any) -> Optional[float]:
    number = _to_decimal(value)
    return float(number) if number is not None else None


def _first_present(data: Dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return None


def normalize_expense_record(record: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {
        "merchant_name": _first_present(record, ["merchant_name", "merchant", "vendor", "store_name"]),
        "transaction_date": _first_present(record, ["transaction_date", "date", "purchase_date"]),
        "currency": _first_present(record, ["currency", "ccy"]),
        "total_amount": _normalize_number(_first_present(record, ["total_amount", "amount", "total", "grand_total"])),
        "tip_amount": _normalize_number(_first_present(record, ["tip_amount", "tip"])),
        "tax_amount": _normalize_number(_first_present(record, ["tax_amount", "tax"])),
        "category": _first_present(record, ["category", "expense_category"]),
        "payment_method": _first_present(record, ["payment_method", "card_type", "payment_type"]),
        "receipt_id": _first_present(record, ["receipt_id", "transaction_id", "id"]),
        "confidence": _normalize_number(_first_present(record, ["confidence", "score"])),
    }
    if normalized["transaction_date"] is None:
        normalized["transaction_date"] = datetime.now(timezone.utc).date().isoformat()
    return normalized


class ExpenseRecordStore:
    def __init__(self, config: Optional[MongoDBAtlasConfig] = None) -> None:
        self.config = config or load_config()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            }
        )

    def store(self, expense_record: Dict[str, Any]) -> Dict[str, Any]:
        normalized = normalize_expense_record(expense_record)
        payload = {
            "dataSource": self.config.data_source,
            "database": self.config.database,
            "collection": self.config.collection,
            "document": {
                **normalized,
                "stored_at": datetime.now(timezone.utc).isoformat(),
            },
        }
        response = self.session.post(
            f"{self.config.base_url}/{self.config.app_id}/endpoint/data/v1/action/insertOne",
            data=json.dumps(payload),
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.json()


def store_expense_record(expense_record: Dict[str, Any]) -> Dict[str, Any]:
    return ExpenseRecordStore().store(expense_record)


def main() -> None:
    import sys

    payload = json.loads(sys.stdin.read() or "{}")
    result = store_expense_record(payload)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
