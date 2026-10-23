import json
from datetime import datetime, timezone
from typing import Any, Optional


class DocumentRequest:
    def __init__(
        self,
        document_id: str,
        data: dict,
        partition_key: Optional[str] = None,
        version: Optional[int] = None,
    ):
        self.document_id = document_id
        self.data = data
        self.partition_key = partition_key or "default"
        self.version = version

    def to_dict(self) -> dict:
        payload = {
            "document_id": self.document_id,
            "partition_key": self.partition_key,
            "data": self.data,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        if self.version is not None:
            payload["version"] = self.version
        return payload


class DocumentResponse:
    def __init__(
        self,
        document_id: str,
        data: dict,
        partition_key: str,
        version: int,
        updated_at: Optional[str] = None,
        found: bool = True,
    ):
        self.document_id = document_id
        self.data = data
        self.partition_key = partition_key
        self.version = version
        self.updated_at = updated_at
        self.found = found

    def to_dict(self) -> dict:
        result = {
            "document_id": self.document_id,
            "partition_key": self.partition_key,
            "data": self.data,
            "version": self.version,
            "found": self.found,
        }
        if self.updated_at:
            result["updated_at"] = self.updated_at
        return result


class QueryResponse:
    def __init__(
        self, documents: list, total_count: int, partition_key: Optional[str] = None
    ):
        self.documents = documents
        self.total_count = total_count
        self.partition_key = partition_key

    def to_dict(self) -> dict:
        result = {
            "documents": [
                doc.to_dict() if hasattr(doc, "to_dict") else doc
                for doc in self.documents
            ],
            "total_count": self.total_count,
        }
        if self.partition_key:
            result["partition_key"] = self.partition_key
        return result


class UpdateResult:
    def __init__(
        self, document_id: str, matched: bool, modified: bool, new_version: int
    ):
        self.document_id = document_id
        self.matched = matched
        self.modified = modified
        self.new_version = new_version

    def to_dict(self) -> dict:
        return {
            "document_id": self.document_id,
            "matched": self.matched,
            "modified": self.modified,
            "new_version": self.new_version,
        }


def normalize_document(raw_doc: dict) -> DocumentResponse:
    data = raw_doc.get("data", raw_doc)
    if isinstance(data, str):
        data = json.loads(data)
    return DocumentResponse(
        document_id=raw_doc.get("document_id", ""),
        data=data,
        partition_key=raw_doc.get("partition_key", "default"),
        version=raw_doc.get("version", 1),
        updated_at=raw_doc.get("updated_at"),
        found=True,
    )


def normalize_query_results(
    raw_results: list, total_count: int, partition_key: Optional[str] = None
) -> QueryResponse:
    docs = [normalize_document(doc) for doc in raw_results]
    return QueryResponse(
        documents=docs, total_count=total_count, partition_key=partition_key
    )
