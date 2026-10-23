from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TextRequest:
    text: str
    model: Optional[str] = None
    system: Optional[str] = None


@dataclass
class QARequest:
    question: str
    context: str
    model: Optional[str] = None


@dataclass
class JSONRequest:
    text: str
    schema_hint: Optional[str] = None
    model: Optional[str] = None


def normalize_json_text(raw: str) -> Dict[str, Any]:
    import json

    return json.loads(raw)


def collect_stream(parts: List[str]) -> str:
    return "".join(parts)
