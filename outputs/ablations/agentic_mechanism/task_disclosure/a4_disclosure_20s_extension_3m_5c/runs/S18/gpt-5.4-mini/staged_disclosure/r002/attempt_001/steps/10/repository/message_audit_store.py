import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


POSTGRES_DSN_ENV = "MESSAGE_AUDIT_POSTGRES_DSN"
POSTGRES_API_URL_ENV = "NEON_POSTGRES_API_URL"
POSTGRES_API_KEY_ENV = "NEON_API_KEY"


@dataclass(frozen=True)
class MessageAuditRecord:
    message_id: str
    status: str
    processed_at: str
    payload: Dict[str, Any]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_record(record: Dict[str, Any]) -> MessageAuditRecord:
    return MessageAuditRecord(
        message_id=str(record.get("message_id", "")),
        status=str(record.get("status", "")),
        processed_at=str(record.get("processed_at") or _utc_now()),
        payload=dict(record.get("payload") or {}),
    )


class NeonPostgresAuditStore:
    def __init__(self, dsn: Optional[str] = None) -> None:
        self.dsn = dsn or os.getenv(POSTGRES_DSN_ENV)
        self.api_url = os.getenv(POSTGRES_API_URL_ENV, "https://console.neon.tech/api/v2")
        self.api_key = os.getenv(POSTGRES_API_KEY_ENV)

    def store_records(self, records: Iterable[Dict[str, Any]]) -> List[MessageAuditRecord]:
        normalized = [_normalize_record(record) for record in records]
        self._persist(normalized)
        return normalized

    def lookup_by_message_id(self, message_id: str) -> Optional[MessageAuditRecord]:
        rows = self._query(
            "SELECT message_id, status, processed_at, payload FROM message_audit WHERE message_id = %s LIMIT 1",
            [message_id],
        )
        if not rows:
            return None
        row = rows[0]
        return MessageAuditRecord(
            message_id=str(row[0]),
            status=str(row[1]),
            processed_at=str(row[2]),
            payload=json.loads(row[3]) if isinstance(row[3], str) else dict(row[3]),
        )

    def recent_records(self, limit: int = 100) -> List[MessageAuditRecord]:
        rows = self._query(
            "SELECT message_id, status, processed_at, payload FROM message_audit ORDER BY processed_at DESC LIMIT %s",
            [int(limit)],
        )
        return [
            MessageAuditRecord(
                message_id=str(row[0]),
                status=str(row[1]),
                processed_at=str(row[2]),
                payload=json.loads(row[3]) if isinstance(row[3], str) else dict(row[3]),
            )
            for row in rows
        ]

    def _persist(self, records: List[MessageAuditRecord]) -> None:
        if self.dsn:
            try:
                import psycopg2

                with psycopg2.connect(self.dsn) as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "CREATE TABLE IF NOT EXISTS message_audit (message_id TEXT PRIMARY KEY, status TEXT NOT NULL, processed_at TIMESTAMPTZ NOT NULL, payload JSONB NOT NULL)"
                        )
                        for record in records:
                            cursor.execute(
                                "INSERT INTO message_audit (message_id, status, processed_at, payload) VALUES (%s, %s, %s, %s) ON CONFLICT (message_id) DO UPDATE SET status = EXCLUDED.status, processed_at = EXCLUDED.processed_at, payload = EXCLUDED.payload",
                                (record.message_id, record.status, record.processed_at, json.dumps(record.payload)),
                            )
                    connection.commit()
                return
            except ImportError:
                pass

        self._persist_via_neon_http(records)

    def _persist_via_neon_http(self, records: List[MessageAuditRecord]) -> None:
        if not self.api_key:
            raise ValueError(f"Missing {POSTGRES_DSN_ENV} or {POSTGRES_API_KEY_ENV}")
        response = requests.post(
            f"{self.api_url.rstrip('/')}/projects",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"records": [asdict(record) for record in records]},
            timeout=30,
        )
        response.raise_for_status()

    def _query(self, sql: str, params: List[Any]) -> List[List[Any]]:
        if self.dsn:
            try:
                import psycopg2
                import psycopg2.extras

                with psycopg2.connect(self.dsn) as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "CREATE TABLE IF NOT EXISTS message_audit (message_id TEXT PRIMARY KEY, status TEXT NOT NULL, processed_at TIMESTAMPTZ NOT NULL, payload JSONB NOT NULL)"
                        )
                        cursor.execute(sql, params)
                        return [list(row) for row in cursor.fetchall()]
            except ImportError:
                pass
        if not self.api_key:
            raise ValueError(f"Missing {POSTGRES_DSN_ENV} or {POSTGRES_API_KEY_ENV}")
        response = requests.post(
            f"{self.api_url.rstrip('/')}/sql",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"query": sql, "params": params},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("rows", [])


def store_message_audit(records: Iterable[Dict[str, Any]]) -> List[MessageAuditRecord]:
    return NeonPostgresAuditStore().store_records(records)
