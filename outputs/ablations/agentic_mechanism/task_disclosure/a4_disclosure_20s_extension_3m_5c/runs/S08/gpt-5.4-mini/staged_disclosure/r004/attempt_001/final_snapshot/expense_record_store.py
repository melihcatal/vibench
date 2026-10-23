import os
from dataclasses import dataclass, asdict
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from google.cloud import firestore


@dataclass(frozen=True)
class ExpenseRecord:
    expense_id: str
    amount: Decimal
    currency: str
    occurred_on: date
    merchant: str
    category: str
    note: Optional[str] = None
    created_at: Optional[datetime] = None


class ExpenseRecordStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "expense_records") -> None:
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.collection_name = collection_name
        self.client = firestore.Client(project=self.project_id)

    def _collection(self):
        return self.client.collection(self.collection_name)

    def normalize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        normalized = {
            "expense_id": str(record["expense_id"]),
            "amount": str(Decimal(str(record["amount"])).quantize(Decimal("0.01"))),
            "currency": str(record["currency"]).upper(),
            "occurred_on": self._normalize_date(record["occurred_on"]),
            "merchant": str(record["merchant"]).strip(),
            "category": str(record["category"]).strip().lower(),
            "note": None if record.get("note") is None else str(record["note"]).strip(),
            "created_at": self._normalize_datetime(record.get("created_at")),
        }
        return {k: v for k, v in normalized.items() if v is not None}

    def save(self, record: Dict[str, Any]) -> str:
        normalized = self.normalize_record(record)
        doc_id = normalized["expense_id"]
        self._collection().document(doc_id).set(normalized)
        return doc_id

    def get(self, expense_id: str) -> Optional[Dict[str, Any]]:
        snap = self._collection().document(str(expense_id)).get()
        if not snap.exists:
            return None
        return snap.to_dict()

    def list(self, limit: int = 100) -> List[Dict[str, Any]]:
        docs = self._collection().limit(limit).stream()
        return [doc.to_dict() for doc in docs]

    def delete(self, expense_id: str) -> None:
        self._collection().document(str(expense_id)).delete()

    @staticmethod
    def _normalize_date(value: Any) -> str:
        if isinstance(value, date):
            return value.isoformat()
        return date.fromisoformat(str(value)).isoformat()

    @staticmethod
    def _normalize_datetime(value: Any) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        return datetime.fromisoformat(str(value)).isoformat()
