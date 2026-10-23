from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import datetime

@dataclass
class StructuredLog:
    message: str
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    service_context: str = "default-service"
    severity: str = "INFO"
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    extra_data: Optional[Dict[str, Any]] = None
