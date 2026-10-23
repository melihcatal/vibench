from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TextRequest:
    text: str
    context: str = ""
    question: str = ""


@dataclass
class JsonExtractionResult:
    data: Dict[str, Any]


@dataclass
class TextResponse:
    text: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_json_text(value: str) -> Dict[str, Any]:
    import json

    return json.loads(value)


def join_chunks(chunks: List[str]) -> str:
    return "".join(chunks)
