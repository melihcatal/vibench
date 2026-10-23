from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class TextRequest:
    prompt: str
    model: Optional[str] = None
    temperature: float = 0.2


@dataclass
class ContextRequest:
    question: str
    context: str
    model: Optional[str] = None
    temperature: float = 0.2


@dataclass
class JsonExtractionRequest:
    text: str
    schema_hint: str
    model: Optional[str] = None
    temperature: float = 0.0


@dataclass
class SafetyReport:
    flagged: bool
    categories: List[str]
    raw: Dict[str, Any]


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None
    model: Optional[str] = None


@dataclass
class EmbeddingRequest:
    texts: List[str]
    model: Optional[str] = None


@dataclass
class SpeechBriefRequest:
    text: str
    model: Optional[str] = None
    voice: str = "alloy"


def parse_json_object(content: str) -> Dict[str, Any]:
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1 or end < start:
        return {"raw": content}
    return json.loads(content[start : end + 1])


def dataclass_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
