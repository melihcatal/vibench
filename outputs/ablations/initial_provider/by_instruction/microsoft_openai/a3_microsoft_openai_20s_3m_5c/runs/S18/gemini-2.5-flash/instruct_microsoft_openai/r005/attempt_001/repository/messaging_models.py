import json
from dataclasses import dataclass, asdict
from typing import Any, Dict

@dataclass
class PubSubEvent:
    id: str
    source: str
    type: str
    specversion: str
    time: str
    data: Dict[str, Any]
    datacontenttype: str = "application/json"

    def to_json(self) -> str:
        return json.dumps(asdict(this))

    @classmethod
    def from_json(cls, json_str: str):
        return cls(**json.loads(json_str))
