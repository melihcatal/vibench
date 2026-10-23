# [HELPER] database_models.py
from typing import TypedDict, Any

# Request models for call signatures


class UpsertRequest(TypedDict):
    doc_id: str
    payload: dict


class FetchRequest(TypedDict):
    doc_id: str


class QueryRequest(TypedDict):
    partition_key: str
    field_name: str
    field_value: Any


class ConditionalUpdateRequest(TypedDict):
    doc_id: str
    update_expr: str
    condition_expr: dict


# Normalization helpers for DynamoDB payloads
def to_dynamodb(item: dict) -> dict:
    """Convert a plain dict to DynamoDB AttributeValue format for PutItem/UpdateItem."""
    return {
        k: {"S": str(v) if isinstance(v, (str, int, float, bool)) else str(v)}
        for k, v in item.items()
    }


def from_dynamodb(item: dict) -> dict:
    """Convert a DynamoDB AttributeValue dict back to plain Python types."""
    return {k: v["S"] for k, v in item.items()}
