from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class StructuredLog:
    message: str
    data: Dict[str, Any]
    severity: str = "INFO"
    correlation_id: str = None
