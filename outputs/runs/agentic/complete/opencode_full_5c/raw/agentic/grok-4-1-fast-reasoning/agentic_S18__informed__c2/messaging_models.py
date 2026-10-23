from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class MessageEvent:
    message_id: Optional[str] = None
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
