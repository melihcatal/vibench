from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime, timezone


@dataclass
class DocumentUpsertRequest:
    document_id: str
    data: dict
    partition_key: Optional[str] = None
    version: Optional[int] = None
    metadata: Optional[dict] = None

    def to_mongo_document(self) -> dict:
        doc = {
            "_id": self.document_id,
            "data": self.data,
            "updated_at": datetime.now(timezone.utc),
        }
        if self.partition_key is not None:
            doc["partition_key"] = self.partition_key
        if self.version is not None:
            doc["version"] = self.version
        if self.metadata is not None:
            doc["metadata"] = self.metadata
        return doc


@dataclass
class DocumentFetchResponse:
    document_id: str
    data: dict
    version: Optional[int] = None
    partition_key: Optional[str] = None
    metadata: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    found: bool = True

    @classmethod
    def from_mongo_document(cls, raw: dict) -> "DocumentFetchResponse":
        return cls(
            document_id=raw.get("_id", ""),
            data=raw.get("data", {}),
            version=raw.get("version"),
            partition_key=raw.get("partition_key"),
            metadata=raw.get("metadata"),
            created_at=raw.get("created_at"),
            updated_at=raw.get("updated_at"),
            found=True,
        )

    @classmethod
    def not_found(cls, document_id: str) -> "DocumentFetchResponse":
        return cls(
            document_id=document_id,
            data={},
            found=False,
        )

    def to_dict(self) -> dict:
        d = asdict(self)
        if self.created_at and isinstance(self.created_at, datetime):
            d["created_at"] = self.created_at.isoformat()
        if self.updated_at and isinstance(self.updated_at, datetime):
            d["updated_at"] = self.updated_at.isoformat()
        return d


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 50
    sort_field: Optional[str] = None
    sort_order: int = -1

    def to_mongo_filter(self) -> dict:
        query = {f"data.{self.field_name}": self.field_value}
        if self.partition_key is not None:
            query["partition_key"] = self.partition_key
        return query


@dataclass
class DocumentQueryResponse:
    documents: list
    total_count: int
    limit: int

    def to_dict(self) -> dict:
        return {
            "documents": [
                d if isinstance(d, dict) else d.to_dict() for d in self.documents
            ],
            "total_count": self.total_count,
            "limit": self.limit,
        }


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    updates: dict
    condition_field: Optional[str] = None
    condition_value: Optional[Any] = None
    expected_version: Optional[int] = None

    def to_mongo_update(self) -> dict:
        update_doc = {"$set": {}}
        for k, v in self.updates.items():
            update_doc["$set"][f"data.{k}"] = v
        update_doc["$set"]["updated_at"] = datetime.now(timezone.utc)
        return update_doc

    def to_mongo_condition(self) -> dict:
        condition = {"_id": self.document_id}
        if self.expected_version is not None:
            condition["version"] = self.expected_version
        if self.condition_field is not None and self.condition_value is not None:
            condition[f"data.{self.condition_field}"] = self.condition_value
        return condition


@dataclass
class ConditionalUpdateResponse:
    document_id: str
    matched: bool
    modified: bool
    new_version: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RecordSummaryRequest:
    document_id: str
    data: dict
    summary_length: str = "medium"

    def to_prompt_fields(self) -> str:
        fields = []
        for k, v in self.data.items():
            fields.append(f"{k}: {v}")
        return "\n".join(fields)


@dataclass
class RecordSummaryResponse:
    document_id: str
    summary: str
    model_used: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TextSafetyRequest:
    document_id: str
    fields_to_check: dict
    categories: Optional[list] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TextSafetyResponse:
    document_id: str
    is_safe: bool
    flags: list
    model_used: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TranslateRequest:
    document_id: str
    fields_to_translate: dict
    target_language: str = "en"
    source_language: str = "auto"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TranslateResponse:
    document_id: str
    translated_fields: dict
    target_language: str
    model_used: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExportArchiveRequest:
    document_id: str
    data: dict
    archive_bucket: Optional[str] = None
    archive_key_prefix: str = "document-archives"
    metadata: Optional[dict] = None

    def to_s3_key(self) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        return f"{self.archive_key_prefix}/{self.document_id}/{timestamp}.json"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExportArchiveResponse:
    document_id: str
    archive_key: str
    archive_bucket: str
    archive_url: Optional[str] = None
    archived: bool = True

    def to_dict(self) -> dict:
        return asdict(self)
