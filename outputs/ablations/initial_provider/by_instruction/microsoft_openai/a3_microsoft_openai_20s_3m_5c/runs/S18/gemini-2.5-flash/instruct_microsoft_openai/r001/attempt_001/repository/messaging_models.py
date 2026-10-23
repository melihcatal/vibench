import json
from dataclasses import dataclass, asdict
from typing import Any, Dict

@dataclass
class EventMessage:
    event_id: str
    event_type: str
    data: Dict[str, Any]
    source: str
    timestamp: str

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str: str):
        return cls(**json.loads(json_str))
