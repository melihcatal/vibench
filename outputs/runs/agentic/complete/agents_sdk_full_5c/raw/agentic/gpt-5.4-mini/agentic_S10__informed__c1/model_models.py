from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TextRequest:
    text: str
    max_output_tokens: int = 256
    temperature: float = 0.2


@dataclass
class ContextQuestionRequest:
    context: str
    question: str
    max_output_tokens: int = 256
    temperature: float = 0.2


@dataclass
class JSONExtractionRequest:
    text: str
    schema_hint: str
    temperature: float = 0.0


@dataclass
class TextResponse:
    text: str
    model: str
    provider: str = "openai"
    raw: Optional[Dict[str, Any]] = None


@dataclass
class StreamingChunk:
    delta: str
    finished: bool = False


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(normalize_text(item) for item in value if normalize_text(item))
    if isinstance(value, dict):
        if "text" in value:
            return normalize_text(value["text"])
        if "content" in value:
            return normalize_text(value["content"])
    return str(value).strip()


def safe_json_object(text: str) -> Dict[str, Any]:
    import json

    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1].rsplit("```", 1)[0]
    return json.loads(cleaned)


def collect_stream_text(chunks: List[StreamingChunk]) -> str:
    return "".join(chunk.delta for chunk in chunks)
