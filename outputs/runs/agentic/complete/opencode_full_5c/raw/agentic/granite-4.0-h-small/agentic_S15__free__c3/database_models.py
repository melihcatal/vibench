# database_models.py
"""
Local helper file defining request, response, and normalization helpers for the Managed NoSQL Document Store.
Provides simple data structures and schema validation utilities.
"""

from pydantic import BaseModel, Field, conlist, validator
from typing import Any, Dict, List, Optional


class Document(BaseModel):
    """Normalized document model used after fetching from the store."""

    id: str = Field(..., description="Primary identifier / partition key")
    created_at: int = Field(
        default_factory=int, description="Unix timestamp of creation"
    )
    updated_at: Optional[int] = Field(None, description="Unix timestamp of last update")
    content: Dict[str, Any] = Field(..., description="User-supplied document fields")
    version: int = Field(default=1, description="Optimistic concurrency version number")

    @validator("version")
    def validate_version(cls, v):
        if v < 1:
            raise ValueError("version must be >= 1")
        return v


class DocumentRequest(BaseModel):
    """Model for creating or updating a document payload."""

    content: Dict[str, Any] = Field(..., description="Document fields to store")
    version: Optional[int] = Field(
        None, description="Optional version for conditional updates"
    )

    def to_dynamodb(self) -> Dict[str, Any]:
        """Convert to a dict suitable for boto3 DynamoDB calls."""
        d = {"content": self.content, "version": self.version or 1}
        if self.version:
            d["version"] = self.version
        return d


def normalize_response(item: Dict[str, Any]) -> Document:
    """Transform a raw DynamoDB item into a Document instance."""

    # DynamoDB may return 'M' (map), 'S' (string), 'N' (number), etc. Basic conversion:
    def convert(value):
        if isinstance(value, dict) and "S" in value:
            return value["S"]
        elif isinstance(value, dict) and "N" in value:
            return int(value["N"])
        elif isinstance(value, dict) and "BOOL" in value:
            return value["BOOL"]
        return value

    normalized = {
        "id": str(item.get("id", "")),
        "created_at": int(item.get("created_at", 0)),
        "updated_at": int(item.get("updated_at", 0)),
        "content": {k: convert(v) for k, v in item.get("content", {}).items()},
        "version": int(item.get("version", 1)),
    }
    try:
        return Document(**normalized)
    except Exception as e:
        raise ValueError(f"Normalization failed: {e}")
