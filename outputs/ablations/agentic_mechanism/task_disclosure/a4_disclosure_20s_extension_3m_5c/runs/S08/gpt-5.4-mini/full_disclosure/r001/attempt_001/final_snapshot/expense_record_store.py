from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", os.getenv("SUPABASE_ANON_KEY", ""))
SUPABASE_TABLE = os.getenv("SUPABASE_EXPENSE_TABLE", "expense_records")


def _coerce_payload(record: Any) -> Dict[str, Any]:
    if isinstance(record, str):
        record = json.loads(record)
    if not isinstance(record, dict):
        raise TypeError("record must be a mapping or JSON string")
    return record


@dataclass(frozen=True)
class ExpenseRecordStoreConfig:
    supabase_url: str
    supabase_service_role_key: str
    table: str = SUPABASE_TABLE

    @classmethod
    def from_env(cls) -> "ExpenseRecordStoreConfig":
        if not SUPABASE_URL:
            raise ValueError("Missing SUPABASE_URL")
        if not SUPABASE_SERVICE_ROLE_KEY:
            raise ValueError("Missing SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY")
        return cls(supabase_url=SUPABASE_URL.rstrip("/"), supabase_service_role_key=SUPABASE_SERVICE_ROLE_KEY, table=SUPABASE_TABLE)


class ExpenseRecordStore:
    def __init__(self, config: Optional[ExpenseRecordStoreConfig] = None) -> None:
        self.config = config or ExpenseRecordStoreConfig.from_env()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self.config.supabase_service_role_key}",
                "apikey": self.config.supabase_service_role_key,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
        )

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "ExpenseRecordStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def save(self, record: Any) -> Dict[str, Any]:
        payload = _coerce_payload(record)
        url = f"{self.config.supabase_url}/rest/v1/{self.config.table}"
        response = self._session.post(url, params={"select": "*"}, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return data[0] if data else {}
        return data if isinstance(data, dict) else {"result": data}


def persist_expense_record(record: Any, config: Optional[ExpenseRecordStoreConfig] = None) -> Dict[str, Any]:
    with ExpenseRecordStore(config=config) as store:
        return store.save(record)
