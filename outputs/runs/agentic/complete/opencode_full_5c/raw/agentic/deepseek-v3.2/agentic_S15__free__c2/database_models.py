from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import json
from datetime import datetime


@dataclass
class DocumentRequest:
    """Request model for document operations."""

    id: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for DynamoDB storage."""
        return {
            "id": self.id,
            "data": self.data,
            "metadata": self.metadata or {},
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentRequest":
        """Create from dictionary."""
        return cls(
            id=data.get("id", ""),
            data=data.get("data", {}),
            metadata=data.get("metadata"),
        )


@dataclass
class DocumentResponse:
    """Response model for document operations."""

    success: bool
    document_id: str
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dynamodb_item(cls, item: Dict[str, Any]) -> "DocumentResponse":
        """Create from DynamoDB item."""
        try:
            document_data = json.loads(item.get("data", {}).get("S", "{}"))
            document_id = item.get("id", {}).get("S", "")

            metadata = {}
            if "created_at" in item:
                metadata["created_at"] = item["created_at"].get("N")
            if "updated_at" in item:
                metadata["updated_at"] = item["updated_at"].get("N")

            return cls(
                success=True,
                document_id=document_id,
                data=document_data,
                metadata=metadata,
            )
        except (json.JSONDecodeError, KeyError) as e:
            return cls(
                success=False,
                document_id="",
                error=f"Failed to parse DynamoDB item: {str(e)}",
            )


@dataclass
class QueryRequest:
    """Request model for query operations."""

    field_name: str
    field_value: Any
    limit: int = 100
    table_name: Optional[str] = None

    def to_dynamodb_params(self, table_name: str) -> Dict[str, Any]:
        """Convert to DynamoDB scan parameters."""
        # Note: This uses scan for simplicity. In production, use GSI for efficient queries.
        return {
            "TableName": table_name,
            "FilterExpression": f"contains(#data, :value)",
            "ExpressionAttributeNames": {"#data": "data"},
            "ExpressionAttributeValues": {
                ":value": {"S": f'"{self.field_name}":"{json.dumps(self.field_value)}"'}
            },
            "Limit": self.limit,
        }


@dataclass
class QueryResponse:
    """Response model for query operations."""

    success: bool
    documents: List[Dict[str, Any]]
    count: int
    scanned_count: int = 0
    error: Optional[str] = None
    last_evaluated_key: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class UpdateRequest:
    """Request model for update operations."""

    document_id: str
    updates: Dict[str, Any]
    condition_expression: Optional[str] = None

    def to_dynamodb_params(
        self, table_name: str, current_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Convert to DynamoDB update parameters."""
        updated_data = {**current_data, **self.updates}

        params = {
            "TableName": table_name,
            "Key": {"id": {"S": self.document_id}},
            "UpdateExpression": "SET #data = :data, #updated_at = :updated_at",
            "ExpressionAttributeNames": {"#data": "data", "#updated_at": "updated_at"},
            "ExpressionAttributeValues": {
                ":data": {"S": json.dumps(updated_data)},
                ":updated_at": {"N": str(int(datetime.utcnow().timestamp()))},
            },
            "ReturnValues": "ALL_NEW",
        }

        if self.condition_expression:
            params["ConditionExpression"] = self.condition_expression

        return params


# Utility functions for data normalization
def normalize_document_data(data: Any) -> Dict[str, Any]:
    """Normalize document data to ensure it's JSON serializable."""
    if isinstance(data, dict):
        return data
    elif isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {"content": data}
    else:
        return {"value": str(data)}


def validate_document_id(document_id: str) -> bool:
    """Validate document ID format."""
    if not document_id or not isinstance(document_id, str):
        return False
    if len(document_id) > 1024:  # DynamoDB key length limit
        return False
    return True


def prepare_dynamodb_item(document_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare a DynamoDB item from document data."""
    timestamp = int(datetime.utcnow().timestamp())

    return {
        "id": {"S": document_id},
        "data": {"S": json.dumps(data)},
        "updated_at": {"N": str(timestamp)},
    }


def parse_dynamodb_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Parse a DynamoDB item back to document data."""
    result = {"id": item.get("id", {}).get("S", ""), "data": {}, "metadata": {}}

    # Parse document data
    data_str = item.get("data", {}).get("S", "{}")
    try:
        result["data"] = json.loads(data_str)
    except json.JSONDecodeError:
        result["data"] = {"raw": data_str}

    # Parse metadata fields
    for key in ["created_at", "updated_at"]:
        if key in item:
            result["metadata"][key] = item[key].get("N")

    return result
