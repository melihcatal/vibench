import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import requests

from document_models import build_standard_expense_schema


DEFAULT_SUPABASE_URL = os.getenv("SUPABASE_URL", "")
DEFAULT_SUPABASE_KEY_ENV = "SUPABASE_SERVICE_ROLE_KEY"
DEFAULT_SUPABASE_TABLE = os.getenv("SUPABASE_EXPENSE_TABLE", "expense_records")
DEFAULT_TIMEOUT = float(os.getenv("EXPENSE_RECORD_STORE_TIMEOUT", "30"))


@dataclass(frozen=True)
class ExpenseRecordStoreConfig:
    supabase_url: str = DEFAULT_SUPABASE_URL
    service_role_key: Optional[str] = None
    table: str = DEFAULT_SUPABASE_TABLE
    timeout: float = DEFAULT_TIMEOUT
    schema: str = "public"
    prefer_representation: bool = True
    extra_headers: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "ExpenseRecordStoreConfig":
        return cls(
            supabase_url=os.getenv("SUPABASE_URL", DEFAULT_SUPABASE_URL),
            service_role_key=os.getenv(DEFAULT_SUPABASE_KEY_ENV),
            table=os.getenv("SUPABASE_EXPENSE_TABLE", DEFAULT_SUPABASE_TABLE),
            timeout=float(os.getenv("EXPENSE_RECORD_STORE_TIMEOUT", str(DEFAULT_TIMEOUT))),
            schema=os.getenv("SUPABASE_SCHEMA", "public"),
        )


class ExpenseRecordStoreError(RuntimeError):
    pass


class ExpenseRecordStore:
    def __init__(self, config: Optional[ExpenseRecordStoreConfig] = None) -> None:
        self.config = config or ExpenseRecordStoreConfig.from_env()
        self._session = requests.Session()

    @property
    def api_key(self) -> str:
        key = self.config.service_role_key or os.getenv(DEFAULT_SUPABASE_KEY_ENV)
        if not key:
            raise ExpenseRecordStoreError(f"Missing API key in {DEFAULT_SUPABASE_KEY_ENV}")
        return key

    @property
    def base_url(self) -> str:
        if not self.config.supabase_url:
            raise ExpenseRecordStoreError("Missing SUPABASE_URL")
        return self.config.supabase_url.rstrip("/")

    @property
    def headers(self) -> Dict[str, str]:
        headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation" if self.config.prefer_representation else "return=minimal",
        }
        headers.update(self.config.extra_headers)
        return headers

    def persist(self, expense_record: Dict[str, Any]) -> Dict[str, Any]:
        normalized = build_standard_expense_schema(expense_record)
        url = f"{self.base_url}/rest/v1/{self.config.table}"
        response = self._session.post(
            url,
            headers=self.headers,
            json=normalized,
            timeout=self.config.timeout,
        )
        if response.status_code >= 400:
            raise ExpenseRecordStoreError(f"{response.status_code} {response.text}")
        if response.content:
            return response.json()[0] if isinstance(response.json(), list) and response.json() else response.json()
        return normalized

    def close(self) -> None:
        self._session.close()
