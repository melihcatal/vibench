import dataclasses
from typing import Any, Dict, Optional


@dataclasses.dataclass
class Document:
    id: str
    data: Dict[str, Any]
    version: Optional[int] = None


@dataclasses.dataclass
class QueryFilter:
    field: str
    value: Any


@dataclasses.dataclass
class UpdateCondition:
    field: str
    operator: str  # e.g., "==", "<", ">"
    value: Any
