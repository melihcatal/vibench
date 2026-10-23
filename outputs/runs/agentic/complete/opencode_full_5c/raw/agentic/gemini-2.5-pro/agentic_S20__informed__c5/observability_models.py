from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class StructuredLog:
    message: str
    user_id: str
    request_id: str
    severity: str = "INFO"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CorrelatedLog:
    message: str
    correlation_id: str
    service_name: str
    severity: str = "INFO"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
