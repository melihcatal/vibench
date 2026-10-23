from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class StructuredLog:
    message: str
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    severity: str = "INFO"
    extra_data: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return asdict(self)


LOG_NAME = "my-application-log"
