import json
import os
from datetime import datetime, timezone

import requests


MONGODB_DATA_API_URL = "https://data.mongodb-api.com/app/data-"


def _clean_text(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return str(value).strip() or None


def _to_iso_date(value):
    value = _clean_text(value)
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def _normalize_expense_record(record):
    if not isinstance(record, dict):
        raise TypeError("expense record must be a mapping")
    normalized = {
        "date": _to_iso_date(record.get("date") or record.get("transaction_date") or record.get("expense_date")),
        "merchant": _clean_text(record.get("merchant") or record.get("vendor") or record.get("payee")),
        "amount": _clean_text(record.get("amount") or record.get("total") or record.get("value")),
        "currency": _clean_text(record.get("currency") or record.get("ccy")),
        "category": _clean_text(record.get("category") or record.get("expense_category")),
        "payment_method": _clean_text(record.get("payment_method") or record.get("card") or record.get("tender")),
        "tax": _clean_text(record.get("tax") or record.get("vat") or record.get("sales_tax")),
        "tip": _clean_text(record.get("tip") or record.get("gratuity")),
        "notes": _clean_text(record.get("notes") or record.get("description") or record.get("memo")),
        "source": _clean_text(record.get("source")) or "external:mongodb-atlas",
    }
    if normalized["currency"]:
        normalized["currency"] = normalized["currency"].upper()
    return normalized


class ExpenseRecordStore:
    def __init__(self, base_url=None, api_key=None, data_source=None, database=None, collection=None):
        self.base_url = (base_url or os.environ.get("MONGODB_DATA_API_BASE_URL") or MONGODB_DATA_API_URL).rstrip("/")
        self.api_key = api_key or os.environ.get("MONGODB_DATA_API_KEY")
        self.data_source = data_source or os.environ.get("MONGODB_DATA_API_DATA_SOURCE")
        self.database = database or os.environ.get("MONGODB_DATA_API_DATABASE")
        self.collection = collection or os.environ.get("MONGODB_DATA_API_COLLECTION")

    def _headers(self):
        if not self.api_key:
            raise RuntimeError("MONGODB_DATA_API_KEY is required")
        return {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

    def _endpoint(self, action):
        if not all([self.data_source, self.database, self.collection]):
            raise RuntimeError("MONGODB_DATA_API_DATA_SOURCE, MONGODB_DATA_API_DATABASE, and MONGODB_DATA_API_COLLECTION are required")
        return f"{self.base_url}/action/{action}"

    def store(self, expense_record):
        document = _normalize_expense_record(expense_record)
        response = requests.post(
            self._endpoint("insertOne"),
            headers=self._headers(),
            json={
                "dataSource": self.data_source,
                "database": self.database,
                "collection": self.collection,
                "document": document,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def store_many(self, expense_records):
        documents = [_normalize_expense_record(record) for record in expense_records]
        response = requests.post(
            self._endpoint("insertMany"),
            headers=self._headers(),
            json={
                "dataSource": self.data_source,
                "database": self.database,
                "collection": self.collection,
                "documents": documents,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def persist_expense_record(expense_record):
    return ExpenseRecordStore().store(expense_record)
