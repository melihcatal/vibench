from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class Item:
    """Represents a single document in the NoSQL database."""
    id: str
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class PutItemRequest:
    """Request to put (create or replace) an item."""
    table_name: str
    item: Item
    
@dataclass
class PutItemResponse:
    """Response after putting an item."""
    success: bool
    item: Optional[Item] = None
    message: Optional[str] = None

@dataclass
class GetItemRequest:
    """Request to get an item by its ID."""
    table_name: str
    item_id: str

@dataclass
class GetItemResponse:
    """Response after getting an item."""
    success: bool
    item: Optional[Item] = None
    message: Optional[str] = None

@dataclass
class UpdateItemRequest:
    """Request to update an existing item."""
    table_name: str
    item_id: str
    updates: Dict[str, Any] # Fields to update and their new values

@dataclass
class UpdateItemResponse:
    """Response after updating an item."""
    success: bool
    item: Optional[Item] = None
    message: Optional[str] = None

def normalize_item_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes item data by removing None values and ensuring consistent types.
    This is a basic example and can be extended based on specific database requirements.
    """
    normalized_data = {}
    for key, value in data.items():
        if value is not None:
            # Example: convert all keys to lowercase, or handle specific types
            normalized_data[key] = value
    return normalized_data

def denormalize_item_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Denormalizes item data from the database into a more application-friendly format.
    This is a basic example and can be extended based on specific application requirements.
    """
    # For now, a simple passthrough. Could involve type conversions,
    # remapping keys, etc.
    return data
