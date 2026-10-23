import dataclasses
from typing import Any, Dict, Optional

@dataclasses.dataclass
class Secret:
    name: str
    value: str
    version: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    annotations: Optional[Dict[str, str]] = None
    metadata: Optional[Dict[str, Any]] = None
