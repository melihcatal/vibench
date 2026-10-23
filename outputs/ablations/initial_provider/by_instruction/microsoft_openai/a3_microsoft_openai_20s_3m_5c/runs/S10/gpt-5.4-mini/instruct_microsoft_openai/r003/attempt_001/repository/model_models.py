import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional


@dataclass
class TextRequest:
    text: str
    style: Optional[str] = None
    temperature: float = 0.2


@dataclass
class ContextQuestionRequest:
    context: str
    question: str
    temperature: float = 0.2


@dataclass
class JsonExtractionRequest:
    text: str
    schema_hint: Optional[str] = None
    temperature: float = 0.0


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return str(value).strip()


def normalize_json_text(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    text = normalize_text(value)
    return json.loads(text)


def streamed_text(chunks: Iterable[Any]) -> str:
    pieces = []
    for chunk in chunks:
        delta = getattr(chunk.choices[0], "delta", None)
        content = getattr(delta, "content", None) if delta is not None else None
        if content:
            pieces.append(content)
    return "".join(pieces)
