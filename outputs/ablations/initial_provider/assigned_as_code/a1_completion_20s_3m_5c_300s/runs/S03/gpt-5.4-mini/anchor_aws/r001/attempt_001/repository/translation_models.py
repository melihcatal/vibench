from dataclasses import dataclass
from typing import Any, Dict, List, Mapping


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def normalize_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    data = dict(payload)
    if "text" in data:
        data["text"] = normalize_text(data["text"])
    if "texts" in data:
        data["texts"] = [normalize_text(item) for item in data["texts"]]
    if "values" in data and isinstance(data["values"], Mapping):
        data["values"] = {key: normalize_text(val) for key, val in data["values"].items()}
    return data


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class TranslationBatchRequest:
    texts: List[str]
    source_language: str
    target_language: str


@dataclass
class TranslationResult:
    text: str
    source_language: str
    target_language: str
