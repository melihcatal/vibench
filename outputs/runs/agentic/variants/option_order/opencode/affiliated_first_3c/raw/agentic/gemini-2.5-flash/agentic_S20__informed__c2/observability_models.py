import dataclasses
from typing import Dict, Any, Optional


@dataclasses.dataclass
class StructuredLog:
    message: str
    severity: str
    component: str
    metadata: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class LogQuery:
    project_id: str
    filter_string: str
    order_by: str = "timestamp desc"
    limit: int = 100
