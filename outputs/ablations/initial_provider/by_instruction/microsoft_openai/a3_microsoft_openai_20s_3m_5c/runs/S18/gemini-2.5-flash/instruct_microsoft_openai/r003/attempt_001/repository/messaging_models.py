import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

@dataclass
class EventMessage:
    event_id: str
    event_type: str
    source: str
    timestamp: str
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def to_json_string(self) -> str:
        return json.dumps(asdict(this))
