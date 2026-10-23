import json
from typing import Any, Dict

class EventMessage:
    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload

    def to_json(self) -> str:
        return json.dumps(self.payload)

    @classmethod
    def from_json(cls, json_string: str):
        return cls(json.loads(json_string))
