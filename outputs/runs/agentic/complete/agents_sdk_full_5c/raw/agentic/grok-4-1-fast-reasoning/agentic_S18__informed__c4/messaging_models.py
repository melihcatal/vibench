from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class PubSubMessage:
    id: str
    data: Dict[str, Any]
    attributes: Dict[str, str]