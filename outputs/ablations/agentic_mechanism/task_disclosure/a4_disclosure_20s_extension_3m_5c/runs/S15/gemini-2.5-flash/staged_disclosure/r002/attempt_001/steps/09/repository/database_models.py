import dataclasses
from typing import Any, Dict, List, Optional, Union

@dataclasses.dataclass
class NoSQLRequest:
    """Base class for NoSQL document store request parameters."""
    pass

@dataclasses.dataclass
class NoSQLResponse:
    """Base class for NoSQL document store response objects."""
    success: bool
    message: Optional[str] = None
    data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None

def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a dictionary item for storage or retrieval from a NoSQL document store.
    This function can be extended to handle specific data type conversions,
    attribute renames, or other normalization logic required by the NoSQL service.
    """
    normalized_data = {}
    for key, value in item.items():
        # Example: Convert specific types if necessary
        # if isinstance(value, datetime):
        #     normalized_data[key] = value.isoformat()
        # else:
        normalized_data[key] = value
    return normalized_data

@dataclasses.dataclass
class PutItemRequest(NoSQLRequest):
    """Request to put (create or update) a single item."""
    table_name: str
    item: Dict[str, Any]

@dataclasses.dataclass
class GetItemRequest(NoSQLRequest):
    """Request to get a single item by its primary key."""
    table_name: str
    key: Dict[str, Any]

@dataclasses.dataclass
class DeleteItemRequest(NoSQLRequest):
    """Request to delete a single item by its primary key."""
    table_name: str
    key: Dict[str, Any]

@dataclasses.dataclass
class QueryRequest(NoSQLRequest):
    """Request to query items based on a condition."""
    table_name: str
    key_condition_expression: str
    expression_attribute_values: Dict[str, Any]
    filter_expression: Optional[str] = None

@dataclasses.dataclass
class ItemResponse(NoSQLResponse):
    """Response for operations involving a single item."""
    data: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class QueryResponse(NoSQLResponse):
    """Response for query operations returning multiple items."""
    data: Optional[List[Dict[str, Any]]] = None
