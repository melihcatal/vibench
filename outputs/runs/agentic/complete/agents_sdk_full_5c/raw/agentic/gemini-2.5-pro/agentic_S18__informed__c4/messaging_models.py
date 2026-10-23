import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class Event:
    event_id: str
    event_type: str
    data: Dict[str, Any]
    source: Optional[str] = "unknown"

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str: str) -> "Event":
        data = json.loads(json_str)
        return cls(**data)
