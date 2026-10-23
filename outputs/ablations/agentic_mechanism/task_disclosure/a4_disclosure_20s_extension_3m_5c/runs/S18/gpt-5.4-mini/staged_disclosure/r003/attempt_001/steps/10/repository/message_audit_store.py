import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pinecone import Pinecone, ServerlessSpec


@dataclass(frozen=True)
class AuditRecord:
    message_id: str
    processed_at: str
    status: str
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MessageAuditStore:
    def __init__(self, index_name: str = "message-audit-store", namespace: str = "default") -> None:
        api_key = os.environ.get("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY is required")
        self._pc = Pinecone(api_key=api_key)
        self._index_name = index_name
        self._namespace = namespace
        self._index = self._ensure_index()

    def _ensure_index(self):
        existing = {idx["name"] for idx in self._pc.list_indexes()}
        if self._index_name not in existing:
            self._pc.create_index(
                name=self._index_name,
                dimension=8,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        return self._pc.Index(self._index_name)

    @staticmethod
    def _vector_from_record(record: AuditRecord) -> List[float]:
        seed = sum(ord(ch) for ch in record.message_id + record.status)
        return [((seed + i * 17) % 1000) / 1000.0 for i in range(8)]

    def persist(self, message_id: str, status: str, source: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> AuditRecord:
        record = AuditRecord(
            message_id=message_id,
            processed_at=datetime.now(timezone.utc).isoformat(),
            status=status,
            source=source,
            metadata=metadata,
        )
        self._index.upsert(
            vectors=[
                {
                    "id": message_id,
                    "values": self._vector_from_record(record),
                    "metadata": {
                        "message_id": record.message_id,
                        "processed_at": record.processed_at,
                        "status": record.status,
                        "source": record.source,
                        "metadata": record.metadata,
                    },
                }
            ],
            namespace=self._namespace,
        )
        return record

    def lookup(self, message_id: str) -> Optional[AuditRecord]:
        result = self._index.fetch(ids=[message_id], namespace=self._namespace)
        vectors = result.get("vectors", {}) if isinstance(result, dict) else getattr(result, "vectors", {})
        item = vectors.get(message_id)
        if not item:
            return None
        md = item.get("metadata", {})
        return AuditRecord(
            message_id=md.get("message_id", message_id),
            processed_at=md.get("processed_at", ""),
            status=md.get("status", ""),
            source=md.get("source"),
            metadata=md.get("metadata"),
        )

    def list_recent(self, limit: int = 10) -> List[AuditRecord]:
        query_vector = [0.0] * 8
        result = self._index.query(vector=query_vector, top_k=limit, include_metadata=True, namespace=self._namespace)
        matches = result.get("matches", []) if isinstance(result, dict) else getattr(result, "matches", [])
        records: List[AuditRecord] = []
        for match in matches:
            md = match.get("metadata", {})
            records.append(
                AuditRecord(
                    message_id=md.get("message_id", match.get("id", "")),
                    processed_at=md.get("processed_at", ""),
                    status=md.get("status", ""),
                    source=md.get("source"),
                    metadata=md.get("metadata"),
                )
            )
        return records
