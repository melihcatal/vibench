from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextRequest:
    text: str
    prompt: Optional[str] = None
    context: Optional[str] = None


@dataclass
class TextResponse:
    text: str
    raw: Any = None


def coerce_json_payload(content: str) -> Dict[str, Any]:
    import json

    return json.loads(content)
