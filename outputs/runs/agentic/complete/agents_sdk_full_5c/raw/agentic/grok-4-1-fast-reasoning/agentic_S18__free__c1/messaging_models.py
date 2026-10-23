import json
from typing import Dict, Any, List

def serialize_event(event: Dict[str, Any]) -> bytes:
    return json.dumps(event, ensure_ascii=False).encode("utf-8")

def deserialize_event(data: bytes) -> Dict[str, Any]:
    return json.loads(data.decode("utf-8"))

Event = Dict[str, Any]
BatchEvents = List[Event]
