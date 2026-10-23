from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import firestore

from document_models import NormalizedExpenseRecord


DEFAULT_COLLECTION = "expense_records"


@dataclass(frozen=True)
class ExpenseRecordStoreConfig:
    project_id: Optional[str] = None
    collection_name: str = DEFAULT_COLLECTION


def load_expense_record_store_config() -> ExpenseRecordStoreConfig:
    return ExpenseRecordStoreConfig(
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT"),
        collection_name=os.environ.get("FIRESTORE_EXPENSE_COLLECTION", DEFAULT_COLLECTION).strip() or DEFAULT_COLLECTION,
    )


class ExpenseRecordStore:
    def __init__(self, client: Optional[firestore.Client] = None, config: Optional[ExpenseRecordStoreConfig] = None) -> None:
        self.config = config or load_expense_record_store_config()
        self._client = client or firestore.Client(project=self.config.project_id)

    def persist(self, record: Dict[str, Any] | NormalizedExpenseRecord, record_id: Optional[str] = None) -> Dict[str, Any]:
        normalized = record.to_dict() if isinstance(record, NormalizedExpenseRecord) else NormalizedExpenseRecord.from_mapping(record).to_dict()
        document_id = record_id or self._build_document_id(normalized)
        payload = dict(normalized)
        payload["stored_at"] = datetime.now(timezone.utc).isoformat()
        self._client.collection(self.config.collection_name).document(document_id).set(payload)
        return {"document_id": document_id, "collection_name": self.config.collection_name, "record": payload}

    def _build_document_id(self, record: Dict[str, Any]) -> str:
        parts = [record.get("vendor_name") or "unknown_vendor", record.get("transaction_date") or "unknown_date", str(record.get("total_amount") or "unknown_total")]
        return "_".join(str(part).strip().replace(" ", "-") for part in parts if str(part).strip()) or f"expense_{int(datetime.now(timezone.utc).timestamp())}"


def persist_expense_record(record: Dict[str, Any] | NormalizedExpenseRecord, record_id: Optional[str] = None) -> Dict[str, Any]:
    return ExpenseRecordStore().persist(record, record_id=record_id)


__all__ = ["ExpenseRecordStore", "ExpenseRecordStoreConfig", "load_expense_record_store_config", "persist_expense_record"]
