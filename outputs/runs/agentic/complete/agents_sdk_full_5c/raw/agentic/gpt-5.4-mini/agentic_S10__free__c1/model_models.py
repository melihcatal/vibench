from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TextRequest:
    text: str
    model: Optional[str] = None


@dataclass
class QuestionContextRequest:
    question: str
    context: str
    model: Optional[str] = None


@dataclass
class ExtractRequest:
    text: str
    schema_hint: str
    model: Optional[str] = None


@dataclass
class TranslateRequest:
    text: str
    target_language: str
    model: Optional[str] = None


@dataclass
class SafetyResult:
    safe: bool
    categories: List[str]
    explanation: str


@dataclass
class EmbeddingRequest:
    text: str
    model: Optional[str] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def parse_json_response(content: str) -> Dict[str, Any]:
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(content[start : end + 1])
        raise
