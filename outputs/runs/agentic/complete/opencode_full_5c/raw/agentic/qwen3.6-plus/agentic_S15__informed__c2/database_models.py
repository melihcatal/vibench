from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass
class DocumentRequest:
    document_id: str
    data: dict[str, Any]
    partition_key: str | None = None
    version: int | None = None

    def to_mongo_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "_id": self.document_id,
            "data": self.data,
            "updated_at": datetime.now(timezone.utc),
        }
        if self.partition_key is not None:
            payload["partition_key"] = self.partition_key
        if self.version is not None:
            payload["version"] = self.version
        return payload


@dataclass
class DocumentResponse:
    document_id: str
    data: dict[str, Any]
    partition_key: str | None = None
    version: int | None = None
    found: bool = True
    updated_at: str | None = None

    @classmethod
    def from_mongo(cls, doc: dict[str, Any] | None) -> DocumentResponse:
        if doc is None:
            return cls(
                document_id="",
                data={},
                found=False,
            )
        return cls(
            document_id=doc.get("_id", ""),
            data=doc.get("data", {}),
            partition_key=doc.get("partition_key"),
            version=doc.get("version"),
            found=True,
            updated_at=str(doc.get("updated_at", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class QueryResponse:
    documents: list[DocumentResponse]
    total_count: int

    @classmethod
    def from_cursor(cls, cursor, max_results: int = 100) -> QueryResponse:
        docs = []
        count = 0
        for doc in cursor:
            if count >= max_results:
                break
            docs.append(DocumentResponse.from_mongo(doc))
            count += 1
        return cls(documents=docs, total_count=count)


@dataclass
class UpdateResult:
    document_id: str
    matched: bool
    modified: bool
    new_version: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_document_id(raw_id: str) -> str:
    return raw_id.strip() or str(uuid.uuid4())


def build_conditional_filter(field: str, operator: str, value: Any) -> dict[str, Any]:
    mongo_ops = {
        "gt": "$gt",
        "gte": "$gte",
        "lt": "$lt",
        "lte": "$lte",
        "eq": "$eq",
        "ne": "$ne",
    }
    op = mongo_ops.get(operator, "$eq")
    return {field: {op: value}}
