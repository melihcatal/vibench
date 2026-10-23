import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests


class MessageAuditStore:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (base_url or os.getenv("SUPABASE_URL") or "").rstrip("/")
        self.api_key = api_key or os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY") or ""
        self.table = os.getenv("SUPABASE_AUDIT_TABLE", "message_audit_records")

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["apikey"] = self.api_key
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def persist(self, record: Dict[str, Any]) -> Dict[str, Any]:
        payload = dict(record)
        payload.setdefault("created_at", datetime.now(timezone.utc).isoformat())
        if not self.base_url:
            raise ValueError("SUPABASE_URL is required")
        response = requests.post(
            f"{self.base_url}/rest/v1/{self.table}",
            headers={**self._headers(), "Prefer": "return=representation"},
            data=json.dumps(payload),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data[0] if isinstance(data, list) and data else data

    def lookup(self, message_id: str) -> Any:
        if not self.base_url:
            raise ValueError("SUPABASE_URL is required")
        response = requests.get(
            f"{self.base_url}/rest/v1/{self.table}",
            headers=self._headers(),
            params={"message_id": f"eq.{message_id}", "limit": 1},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data[0] if isinstance(data, list) and data else None
