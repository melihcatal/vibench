from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    system: Optional[str] = None
    max_tokens: int = 256
    temperature: float = 0.2
    top_p: float = 0.95


@dataclass
class PlatformResource:
    project_id: str
    location: str
    publisher: str
    model: str

    @property
    def full_model_name(self) -> str:
        return f"projects/{self.project_id}/locations/{self.location}/publishers/{self.publisher}/models/{self.model}"


@dataclass
class PlatformTextChunk:
    text: str
    candidate_index: int = 0
    raw: Any = None


@dataclass
class PlatformResponse:
    text: str
    model: str
    resource_name: str
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


def to_vertex_contents(request: PlatformRequest) -> List[Dict[str, Any]]:
    contents: List[Dict[str, Any]] = []
    if request.system:
        contents.append({"role": "user", "parts": [{"text": request.system}]})
    contents.append({"role": "user", "parts": [{"text": request.prompt}]})
    return contents


def normalize_vertex_text(response: Any) -> str:
    if hasattr(response, "text") and response.text:
        return response.text
    candidates = getattr(response, "candidates", None) or []
    parts: List[str] = []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        if not content:
            continue
        for part in getattr(content, "parts", []) or []:
            text = getattr(part, "text", None)
            if text:
                parts.append(text)
    return "".join(parts)


def normalize_usage_metadata(response: Any) -> Dict[str, Any]:
    usage = getattr(response, "usage_metadata", None)
    if usage is None:
        return {}
    keys = [
        "prompt_token_count",
        "candidates_token_count",
        "total_token_count",
        "cached_content_token_count",
    ]
    return {
        key: getattr(usage, key, None)
        for key in keys
        if getattr(usage, key, None) is not None
    }


def join_stream_text(chunks: Iterable[PlatformTextChunk]) -> str:
    return "".join(chunk.text for chunk in chunks if chunk.text)
