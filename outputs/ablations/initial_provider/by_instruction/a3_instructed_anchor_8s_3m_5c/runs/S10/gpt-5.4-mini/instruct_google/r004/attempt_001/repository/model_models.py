from dataclasses import dataclass
from typing import Any, Iterable


@dataclass
class TextResult:
    text: str


@dataclass
class JsonResult:
    data: dict[str, Any]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, Iterable):
        return "".join(str(part) for part in value).strip()
    return str(value).strip()


def normalize_json_text(value: str) -> dict[str, Any]:
    import json

    return json.loads(value)
