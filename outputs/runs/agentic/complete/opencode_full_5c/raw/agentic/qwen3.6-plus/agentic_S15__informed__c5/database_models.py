from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime, timezone


@dataclass
class DocumentRequest:
    document_id: str
    data: dict
    partition_key: str = "document_id"
    sort_key: Optional[str] = None
    sort_value: Optional[str] = None
    version: Optional[int] = None
    ttl_seconds: Optional[int] = None

    def to_dynamodb_item(self):
        item = {self.partition_key: self.document_id}
        item.update(self.data)
        if self.sort_key and self.sort_value is not None:
            item[self.sort_key] = self.sort_value
        if self.ttl_seconds is not None:
            item["ttl"] = int(datetime.now(timezone.utc).timestamp()) + self.ttl_seconds
        return item


@dataclass
class DocumentResponse:
    document_id: str
    data: dict
    metadata: dict = field(default_factory=dict)
    found: bool = True
    version: Optional[int] = None

    @classmethod
    def from_dynamodb_item(cls, item, partition_key="document_id"):
        if item is None:
            return cls(document_id="", data={}, found=False)
        doc_id = item.get(partition_key, "")
        metadata = {}
        reserved_keys = {partition_key, "ttl", "version", "_version"}
        data = {k: v for k, v in item.items() if k not in reserved_keys}
        version = item.get("version") or item.get("_version")
        if "ttl" in item:
            metadata["ttl"] = item["ttl"]
        return cls(
            document_id=doc_id,
            data=data,
            metadata=metadata,
            found=True,
            version=version,
        )


@dataclass
class QueryResult:
    items: list
    count: int
    last_evaluated_key: Optional[dict] = None

    @classmethod
    def from_dynamodb_response(cls, response, partition_key="document_id"):
        items = []
        for item in response.get("Items", []):
            doc_resp = DocumentResponse.from_dynamodb_item(item, partition_key)
            items.append(doc_resp)
        return cls(
            items=items,
            count=len(items),
            last_evaluated_key=response.get("LastEvaluatedKey"),
        )


@dataclass
class UpdateResult:
    document_id: str
    success: bool
    version: Optional[int] = None
    error: Optional[str] = None
    condition_check_failed: bool = False


@dataclass
class UpsertResult:
    document_id: str
    success: bool
    version: int = 1
    error: Optional[str] = None


def normalize_document_payload(raw_data, document_id, partition_key="document_id"):
    cleaned = {}
    for k, v in raw_data.items():
        if k == partition_key:
            continue
        cleaned[k] = v
    return DocumentRequest(
        document_id=document_id,
        data=cleaned,
        partition_key=partition_key,
    )


def format_query_filter(field_name, field_value):
    from boto3.dynamodb.conditions import Attr

    return Attr(field_name).eq(field_value)
