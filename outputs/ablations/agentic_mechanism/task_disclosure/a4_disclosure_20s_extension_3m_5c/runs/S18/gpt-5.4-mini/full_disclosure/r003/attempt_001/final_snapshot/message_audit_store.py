import os
import sqlite3
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class MessageAuditRecord:
    message_id: str
    status: str
    provider: str
    payload: str
    metadata: Dict[str, Any]
    processed_at: str


class MessageAuditStore:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path or os.environ.get("POSTGRES_AUDIT_DSN", ":memory:")
        self._lock = threading.Lock()
        self._uses_postgres = self.db_path != ":memory:" and self.db_path.startswith("postgresql")
        self._conn = None
        if self._uses_postgres:
            import psycopg2

            self._conn = psycopg2.connect(self.db_path)
        else:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock:
            cur = self._conn.cursor()
            if self._uses_postgres:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS message_audit (
                        message_id TEXT PRIMARY KEY,
                        status TEXT NOT NULL,
                        provider TEXT NOT NULL,
                        payload TEXT NOT NULL,
                        metadata TEXT NOT NULL,
                        processed_at TEXT NOT NULL
                    )
                    """
                )
            else:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS message_audit (
                        message_id TEXT PRIMARY KEY,
                        status TEXT NOT NULL,
                        provider TEXT NOT NULL,
                        payload TEXT NOT NULL,
                        metadata TEXT NOT NULL,
                        processed_at TEXT NOT NULL
                    )
                    """
                )
            self._conn.commit()

    def save(self, message_id: str, status: str, payload: str, metadata: Optional[Dict[str, Any]] = None, provider: str = "aws_sqs") -> MessageAuditRecord:
        record = MessageAuditRecord(
            message_id=message_id,
            status=status,
            provider=provider,
            payload=payload,
            metadata=metadata or {},
            processed_at=datetime.now(timezone.utc).isoformat(),
        )
        with self._lock:
            cur = self._conn.cursor()
            if self._uses_postgres:
                cur.execute(
                    """
                    INSERT INTO message_audit (message_id, status, provider, payload, metadata, processed_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (message_id) DO UPDATE SET
                        status = EXCLUDED.status,
                        provider = EXCLUDED.provider,
                        payload = EXCLUDED.payload,
                        metadata = EXCLUDED.metadata,
                        processed_at = EXCLUDED.processed_at
                    """,
                    (record.message_id, record.status, record.provider, record.payload, str(record.metadata), record.processed_at),
                )
            else:
                cur.execute(
                    """
                    INSERT OR REPLACE INTO message_audit (message_id, status, provider, payload, metadata, processed_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (record.message_id, record.status, record.provider, record.payload, str(record.metadata), record.processed_at),
                )
            self._conn.commit()
        return record

    def get(self, message_id: str) -> Optional[MessageAuditRecord]:
        with self._lock:
            cur = self._conn.cursor()
            if self._uses_postgres:
                cur.execute("SELECT message_id, status, provider, payload, metadata, processed_at FROM message_audit WHERE message_id = %s", (message_id,))
            else:
                cur.execute("SELECT message_id, status, provider, payload, metadata, processed_at FROM message_audit WHERE message_id = ?", (message_id,))
            row = cur.fetchone()
        if not row:
            return None
        return MessageAuditRecord(
            message_id=row[0],
            status=row[1],
            provider=row[2],
            payload=row[3],
            metadata={"raw": row[4]},
            processed_at=row[5],
        )

    def list_recent(self, limit: int = 100) -> List[MessageAuditRecord]:
        with self._lock:
            cur = self._conn.cursor()
            query = "SELECT message_id, status, provider, payload, metadata, processed_at FROM message_audit ORDER BY processed_at DESC LIMIT ?"
            params = (limit,)
            if self._uses_postgres:
                query = "SELECT message_id, status, provider, payload, metadata, processed_at FROM message_audit ORDER BY processed_at DESC LIMIT %s"
            cur.execute(query, params)
            rows = cur.fetchall()
        return [
            MessageAuditRecord(
                message_id=row[0],
                status=row[1],
                provider=row[2],
                payload=row[3],
                metadata={"raw": row[4]},
                processed_at=row[5],
            )
            for row in rows
        ]
