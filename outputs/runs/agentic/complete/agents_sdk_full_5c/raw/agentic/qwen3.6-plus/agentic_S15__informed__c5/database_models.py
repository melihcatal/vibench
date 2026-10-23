"""
Local request, response, and normalization helpers for Amazon DynamoDB
document store operations.

Provides dataclasses and helper functions for building put/get/update
payloads, normalizing responses, and converting between plain JSON and
the DynamoDB wire format.
"""

import json
import datetime
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class DocumentPutRequest:
    """Request payload for upserting a document into DynamoDB."""
    document_id: str
    partition_key: str = "doc_id"
    sort_key: Optional[str] = None
    sort_key_name: str = "doc_version"
    payload: Dict[str, Any] = field(default_factory=dict)
    ttl_seconds: Optional[int] = None
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_item(self) -> Dict[str, Any]:
        """Convert to a plain Python dict suitable for DynamoDB put_item."""
        item = {
            self.partition_key: self.document_id,
        }
        if self.sort_key:
            item[self.sort_key_name] = self.sort_key
        if self.payload:
            for k, v in self.payload.items():
                if k not in (self.partition_key, self.sort_key_name):
                    item[k] = v
        if self.ttl_seconds:
            now = datetime.datetime.now(datetime.timezone.utc)
            item["ttl"] = int(now.timestamp()) + self.ttl_seconds
        if self.metadata:
            item["metadata"] = self.metadata
        item["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        return item


@dataclass
class DocumentFetchRequest:
    """Request payload for fetching a single document."""
    document_id: str
    partition_key: str = "doc_id"
    sort_key: Optional[str] = None
    sort_key_name: str = "doc_version"
    consistent_read: bool = False
    projection_expression: Optional[str] = None

    def to_key(self) -> Dict[str, Any]:
        """Build the DynamoDB key dict for get_item."""
        key = {self.partition_key: self.document_id}
        if self.sort_key:
            key[self.sort_key_name] = self.sort_key
        return key


@dataclass
class DocumentQueryRequest:
    """Request payload for querying documents by a field value or partition key."""
    partition_key_value: str
    partition_key: str = "doc_id"
    filter_field: Optional[str] = None
    filter_value: Optional[Any] = None
    limit: int = 100
    scan_index_forward: bool = True

    def build_kwargs(self) -> Dict[str, Any]:
        """Build kwargs suitable for boto3 Table.query()."""
        from boto3.dynamodb.conditions import Key, Attr
        kwargs = {
            "KeyConditionExpression": Key(self.partition_key).eq(self.partition_key_value),
            "ScanIndexForward": self.scan_index_forward,
            "Limit": self.limit,
        }
        if self.filter_field and self.filter_value is not None:
            kwargs["FilterExpression"] = Attr(self.filter_field).eq(self.filter_value)
        return kwargs


@dataclass
class DocumentUpdateRequest:
    """Request payload for conditional / version-aware updates."""
    document_id: str
    partition_key: str = "doc_id"
    updates: Dict[str, Any] = field(default_factory=dict)
    expected_version: Optional[str] = None
    condition_expression: Optional[str] = None
    expression_attribute_names: Optional[Dict[str, str]] = None
    expression_attribute_values: Optional[Dict[str, Any]] = None

    def build_kwargs(self) -> Dict[str, Any]:
        """Build kwargs suitable for boto3 Table.update_item()."""
        update_parts = []
        attr_values = {}
        attr_names = {}
        idx = 0

        for field_name, field_value in self.updates.items():
            if field_value is None:
                # Use REMOVE to delete the attribute
                update_parts.append(f"REMOVE #{field_name}")
                attr_names[f"#{field_name}"] = field_name
                continue
            placeholder_val = f":v{idx}"
            placeholder_name = f"#f{idx}"
            update_parts.append(f"{placeholder_name} = {placeholder_val}")
            attr_values[placeholder_val] = field_value
            attr_names[placeholder_name] = field_name
            idx += 1

        update_expr = ", ".join(update_parts) if update_parts else "set #noop = :noop"
        if not attr_values and not update_parts:
            attr_values[":noop"] = "noop"

        kwargs: Dict[str, Any] = {
            "Key": {self.partition_key: self.document_id},
            "UpdateExpression": f"SET {update_expr}" if "REMOVE" not in " ".join(update_parts) else update_expr,
            "ExpressionAttributeNames": attr_names,
            "ReturnValues": "ALL_NEW",
        }

        if attr_values:
            kwargs["ExpressionAttributeValues"] = attr_values

        # Version-aware conditional update
        if self.expected_version is not None:
            kwargs["ConditionExpression"] = "version = :expected_version"
            kwargs.setdefault("ExpressionAttributeValues", {})
            kwargs["ExpressionAttributeValues"][":expected_version"] = self.expected_version

        if self.condition_expression:
            kwargs["ConditionExpression"] = self.condition_expression

        if self.expression_attribute_names:
            kwargs.setdefault("ExpressionAttributeNames", {})
            kwargs["ExpressionAttributeNames"].update(self.expression_attribute_names)

        if self.expression_attribute_values:
            kwargs.setdefault("ExpressionAttributeValues", {})
            kwargs["ExpressionAttributeValues"].update(self.expression_attribute_values)

        # Always increment the version number on successful update
        kwargs["UpdateExpression"] = (
            kwargs.get("UpdateExpression", "").rstrip()
            + ", #ver = if_not_exists(#ver, :zero) + :one"
        )
        kwargs["ExpressionAttributeNames"]["#ver"] = "version"
        kwargs.setdefault("ExpressionAttributeValues", {})
        kwargs["ExpressionAttributeValues"][":zero"] = 0
        kwargs["ExpressionAttributeValues"][":one"] = 1

        # Add updated_at timestamp
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        kwargs["UpdateExpression"] += ", #ua = :ua"
        kwargs["ExpressionAttributeNames"]["#ua"] = "updated_at"
        kwargs["ExpressionAttributeValues"][":ua"] = now

        return kwargs


@dataclass
class DocumentResponse:
    """Normalized response from a document store operation."""
    success: bool
    document: Optional[Dict[str, Any]] = None
    operation: str = ""
    error_code: Optional[str] = None
    message: Optional[str] = None
    version: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class DocumentListResponse:
    """Normalized response from a query or scan operation."""
    success: bool
    documents: List[Dict[str, Any]] = field(default_factory=list)
    operation: str = ""
    error_code: Optional[str] = None
    message: Optional[str] = None
    count: int = 0
    last_evaluated_key: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {k: v for k, v in asdict(self).items() if v is not None}
        result["count"] = len(self.documents)
        return result


def serialize_for_dynamodb(value: Any) -> Any:
    """Serialize Python types into DynamoDB-friendly values.

    boto3 resource-level Table automatically handles conversion, but this
    helper is useful when constructing items at the client level.
    """
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    if isinstance(value, set):
        return list(value)
    return value


def extract_text_fields(document: Dict[str, Any], fields: Optional[List[str]] = None) -> List[str]:
    """Extract user-facing text fields from a document for downstream processing.

    If specific fields are requested, only those are returned. Otherwise,
    common text-bearing fields are extracted.
    """
    if fields:
        return [str(document.get(f, "")) for f in fields if document.get(f)]
    default_fields = ["title", "description", "content", "body", "text", "summary", "notes"]
    return [str(document.get(f, "")) for f in default_fields if document.get(f)]
