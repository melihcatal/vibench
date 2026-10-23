from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import json
from datetime import datetime


@dataclass
class DocumentRequest:
    """Request model for document operations."""

    document_id: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

    def to_dynamodb_item(self) -> Dict[str, Any]:
        """Convert to DynamoDB item format."""
        item = {
            "document_id": self.document_id,
            "data": json.dumps(self.data),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        if self.metadata:
            item["metadata"] = json.dumps(self.metadata)

        return item

    @classmethod
    def from_dynamodb_item(cls, item: Dict[str, Any]) -> "DocumentRequest":
        """Create from DynamoDB item."""
        data = json.loads(item.get("data", "{}"))
        metadata = None
        if "metadata" in item:
            metadata = json.loads(item["metadata"])

        return cls(document_id=item.get("document_id"), data=data, metadata=metadata)


@dataclass
class DocumentResponse:
    """Response model for document operations."""

    success: bool
    document_id: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class QueryRequest:
    """Request model for query operations."""

    field_name: str
    field_value: str
    index_name: Optional[str] = None
    limit: int = 100

    def to_dynamodb_params(self, table_name: str) -> Dict[str, Any]:
        """Convert to DynamoDB query parameters."""
        params = {
            "TableName": table_name,
            "KeyConditionExpression": f"{self.field_name} = :val",
            "ExpressionAttributeValues": {":val": self.field_value},
            "Limit": self.limit,
        }

        if self.index_name:
            params["IndexName"] = self.index_name

        return params


@dataclass
class QueryResponse:
    """Response model for query operations."""

    success: bool
    documents: List[Dict[str, Any]]
    count: int
    error: Optional[str] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class DocumentNormalizer:
    """Helper class for normalizing document data."""

    @staticmethod
    def normalize_data(data: Any) -> Dict[str, Any]:
        """Normalize document data to ensure it's JSON serializable."""
        if isinstance(data, dict):
            return {
                str(k): DocumentNormalizer.normalize_data(v) for k, v in data.items()
            }
        elif isinstance(data, list):
            return [DocumentNormalizer.normalize_data(item) for item in data]
        elif isinstance(data, (str, int, float, bool, type(None))):
            return data
        else:
            return str(data)

    @staticmethod
    def validate_document_id(document_id: str) -> bool:
        """Validate document ID format."""
        if not document_id or not isinstance(document_id, str):
            return False
        if len(document_id) > 255:
            return False
        # Basic validation - can be extended
        return True

    @staticmethod
    def extract_fields(data: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """Extract specific fields from document data."""
        result = {}
        for field in fields:
            if field in data:
                result[field] = data[field]
        return result
