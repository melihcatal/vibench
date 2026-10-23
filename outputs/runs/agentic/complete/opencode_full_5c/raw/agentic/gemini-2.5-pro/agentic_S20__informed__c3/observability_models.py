from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import uuid


@dataclass
class LogEntry:
    message: str
    severity: str = "INFO"
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    extra_data: Optional[Dict[str, Any]] = None
