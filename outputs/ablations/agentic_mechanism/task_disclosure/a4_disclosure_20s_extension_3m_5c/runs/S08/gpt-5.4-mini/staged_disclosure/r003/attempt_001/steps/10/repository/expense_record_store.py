import os
from dataclasses import dataclass, asdict
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Dict, Optional

from google.cloud import firestore


def _normalize_amount(value: Any) -> str:
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, (int, float)):
        return format(Decimal(str(value)), "f")
    if isinstance(value, str):
        return format(Decimal(value), "f")
    raise TypeError("amount must be numeric or a numeric string")


def _normalize_timestamp(value: Any) -> str:
    if value is None:
        return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(microsecond=0).isoformat() + "Z"
        return value.astimezone().replace(microsecond=0).isoformat()
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day).isoformat() + "Z"
    if isinstance(value, str):
        return value
    raise TypeError("timestamp must be a datetime, date, string, or None")


def normalize_expense_record(record: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(record)
    if "amount" in normalized:
        normalized["amount"] = _normalize_amount(normalized["amount"])
    if "currency" in normalized and normalized["currency"] is not None:
        normalized["currency"] = str(normalized["currency"]).upper()
    if "merchant" in normalized and normalized["merchant"] is not None:
        normalized["merchant"] = str(normalized["merchant"]).strip()
    if "category" in normalized and normalized["category"] is not None:
        normalized["category"] = str(normalized["category"]).strip().lower()
    if "occurred_at" in normalized:
        normalized["occurred_at"] = _normalize_timestamp(normalized["occurred_at"])
    normalized.setdefault("provider", "google-cloud-firestore")
    normalized.setdefault("normalized", True)
    return normalized


@dataclass
class ExpenseRecordStore:
    project_id: Optional[str] = None
    collection_name: str = "expense_records"

    def __post_init__(self) -> None:
        self.project_id = self.project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
        self._client = firestore.Client(project=self.project_id) if self.project_id else firestore.Client()

    def save(self, record: Dict[str, Any], document_id: Optional[str] = None) -> str:
        normalized = normalize_expense_record(record)
        doc_ref = self._client.collection(self.collection_name).document(document_id) if document_id else self._client.collection(self.collection_name).document()
        doc_ref.set(normalized)
        return doc_ref.id

    def get(self, document_id: str) -> Optional[Dict[str, Any]]:
        snapshot = self._client.collection(self.collection_name).document(document_id).get()
        return snapshot.to_dict() if snapshot.exists else None
