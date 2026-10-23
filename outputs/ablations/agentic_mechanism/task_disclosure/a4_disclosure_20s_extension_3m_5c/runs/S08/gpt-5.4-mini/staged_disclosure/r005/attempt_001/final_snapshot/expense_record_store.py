import os
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional

import requests


MONGODB_DATA_API_URL = "https://data.mongodb-api.com/app/data-0-abcdef/endpoint/data/v1/action"
MONGODB_API_VERSION = "v1"
MONGODB_DATA_SOURCE = os.getenv("MONGODB_DATA_SOURCE", "Cluster0")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "expenses")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "expense_records")


def _to_decimal_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (int, float, Decimal)):
        try:
            return format(Decimal(str(value)).quantize(Decimal("0.01")), "f")
        except InvalidOperation:
            return None
    text = str(value).strip()
    if not text:
        return None
    cleaned = "".join(ch for ch in text if ch.isdigit() or ch in ".-,")
    if cleaned.count(",") > 0 and cleaned.count(".") == 0:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    else:
        cleaned = cleaned.replace(",", "")
    try:
        return format(Decimal(cleaned).quantize(Decimal("0.01")), "f")
    except InvalidOperation:
        return None


def _normalize_date(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    text = str(value).strip()
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%m-%d-%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def normalize_expense_record(record: Dict[str, Any]) -> Dict[str, Any]:
    vendor = record.get("vendor") or record.get("merchant") or record.get("payee")
    amount = _to_decimal_string(record.get("amount") or record.get("total") or record.get("expense_amount"))
    currency = str(record.get("currency") or record.get("currency_code") or "USD").upper()
    date = _normalize_date(record.get("date") or record.get("transaction_date") or record.get("purchase_date"))
    category = record.get("category") or record.get("expense_category") or "uncategorized"
    receipt_id = record.get("receipt_id") or record.get("id") or record.get("document_id")

    normalized = {
        "schema_version": "1.0",
        "vendor": vendor,
        "amount": amount,
        "currency": currency,
        "date": date,
        "category": category,
        "receipt_id": receipt_id,
        "normalized_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    return {k: v for k, v in normalized.items() if v is not None}


@dataclass(frozen=True)
class MongoDBAtlasConfig:
    api_key: str
    data_source: str = MONGODB_DATA_SOURCE
    database: str = MONGODB_DATABASE
    collection: str = MONGODB_COLLECTION
    base_url: str = MONGODB_DATA_API_URL


def load_config() -> MongoDBAtlasConfig:
    api_key = os.getenv("MONGODB_API_KEY", "").strip()
    if not api_key:
        raise ValueError("MONGODB_API_KEY is required")
    data_source = os.getenv("MONGODB_DATA_SOURCE", MONGODB_DATA_SOURCE).strip()
    database = os.getenv("MONGODB_DATABASE", MONGODB_DATABASE).strip()
    collection = os.getenv("MONGODB_COLLECTION", MONGODB_COLLECTION).strip()
    base_url = os.getenv("MONGODB_DATA_API_URL", MONGODB_DATA_API_URL).strip()
    return MongoDBAtlasConfig(api_key=api_key, data_source=data_source, database=database, collection=collection, base_url=base_url)


class ExpenseRecordStore:
    def __init__(self, config: Optional[MongoDBAtlasConfig] = None) -> None:
        self.config = config or load_config()
        self._session = requests.Session()
        self._session.headers.update({"api-key": self.config.api_key, "Content-Type": "application/json"})

    def save(self, record: Dict[str, Any]) -> Dict[str, Any]:
        normalized = normalize_expense_record(record)
        payload = {
            "dataSource": self.config.data_source,
            "database": self.config.database,
            "collection": self.config.collection,
            "document": normalized,
        }
        response = self._session.post(f"{self.config.base_url}/insertOne", json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return {"normalized_record": normalized, "provider_result": result}

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "ExpenseRecordStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
