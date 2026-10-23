from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Secret:
    name: str
    value: Optional[str] = None
    arn: Optional[str] = None
    version_id: Optional[str] = None
    created_date: Optional[Any] = None
    tags: Optional[Dict[str, str]] = None
    metadata: Optional[Dict[str, Any]] = None
