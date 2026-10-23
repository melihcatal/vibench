# database_models.py
"""
Local helper file.

Defines request/response data structures and normalization helpers for the Managed NoSQL Document Store.
"""

from __future__ import annotations
from typing import Any, Dict, List, Union

class DocumentModel:
    """
    Represents a document that will be stored in the NoSQL store.

    Attributes:
        id (str): Primary identifier.
        data (dict): Free‑form JSON payload.
        version (int): Optional optimistic‑concurrency version.
    """

    def __init__(self, id: str, data: dict, version: int = 1):
        self.id = id
        self.data = data
        self.version = version

    def to_dynamodb_item(self) -> Dict[str, Any]:
        """Convert to a structure expected by boto3 Table.put_item / update_item."""
        item: Dict[str, Any] = {"
            PRIMARY_KEY_NAME: self.id,
            "version": {"N": str(self.version)}
        }
        # Merge user data while preserving type hints for strings/numbers/binary/etc.
        for k, v in self.data.items():
            # Simple mapping: str/number -> DynamoDB Scalar, list -> L, dict -> M, bytes -> B
            if isinstance(v, str):
                item[k] = {"S": v}
            elif isinstance(v, (int, float)):
                item[k] = {"N": str(v)}
            elif isinstance(v, bytes):
                item[k] = {"B": v}
            elif isinstance(v, list):
                item[k] = {"L": [self._field_to_dynamo(x) for x in v]}
            elif isinstance(v, dict):
                item[k] = {"M": {k2: self._field_to_dynamo(v2) for k2, v2 in v.items()}}
            else:
                item[k] = {"S": str(v)}
        return item

    @staticmethod
    def _field_to_dynamo(value: Any) -> Any:
        if isinstance(value, str):
            return {"S": value}
        elif isinstance(value, (int, float)):
            return {"N": str(value)}
        elif isinstance(value, bytes):
            return {"B": value}
        elif isinstance(value, list):
            return {"L": [DocumentModel._field_to_dynamo(x) for x in value]}
        elif isinstance(value, dict):
            return {"M": {k: DocumentModel._field_to_dynamo(v) for k, v in value.items()}}
        else:
            return {"S": str(value)}


class DocumentResponse:
    """Response wrapper for a fetched document."""

    def __init__(self, item: dict):
        self.item = item

    @property
    def id(self) -> str:
        return self.item.get(PRIMARY_KEY_NAME)

    @property
    def data(self) -> dict:
        # Convert DynamoDB attribute map back to plain dict
        result: dict = {}
        for k, v in self.item.items():
            if k == PRIMARY_KEY_NAME:
                continue
            result[k] = self._value_from_dynamo(v)
        return result

    @staticmethod
    def _value_from_dynamo(attr: dict) -> Any:
        if "S" in attr:
            return attr["S"]
        if "N" in attr:
            return int(attr["N"]) if "." not in attr["N"] else float(attr["N"])  # preserve decimal if needed
        if "B" in attr:
            return attr["B"]
        if "L" in attr:
            return [DocumentModel._value_from_dynamo(x) for x in attr["L"]]
        if "M" in attr:
            return {k: DocumentModel._value_from_dynamo(v) for k, v in attr["M"].items()}
        # Fallback
        return attr.get("S", "")
