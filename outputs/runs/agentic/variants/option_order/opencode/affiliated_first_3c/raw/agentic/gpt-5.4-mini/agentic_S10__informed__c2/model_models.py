from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import json


@dataclass
class GenerationRequest:
    prompt: str
    system: str = ""
    temperature: float = 0.2
    max_tokens: int = 512


@dataclass
class GenerationResponse:
    text: str
    model: str
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def parse_json_text(text: str) -> Dict[str, Any]:
    return json.loads(text)


def build_json_schema(fields: List[str]) -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {field: {"type": "string"} for field in fields},
        "required": fields,
    }
