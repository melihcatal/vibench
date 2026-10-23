from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CompletionRequest:
    model: str
    messages: List[Dict[str, str]]
    temperature: float = 0.0
    stream: bool = False
    response_format: Optional[Dict[str, Any]] = None

    def to_openai_kwargs(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "stream": self.stream,
        }
        if self.response_format is not None:
            payload["response_format"] = self.response_format
        return payload


@dataclass
class CompletionResponse:
    text: str
    model: Optional[str] = None
    raw: Any = None


@dataclass
class NormalizedEmbeddingResponse:
    model: Optional[str]
    vector: List[float]
    raw: Any = None


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    raw: Any = None


def normalize_completion_response(resp: Any) -> CompletionResponse:
    choice = resp.choices[0]
    text = getattr(choice.message, "content", None) or ""
    return CompletionResponse(text=text, model=getattr(resp, "model", None), raw=resp)


def normalize_moderation_response(resp: Any) -> ModerationResult:
    result = resp.results[0]
    return ModerationResult(flagged=bool(result.flagged), categories=dict(getattr(result, "categories", {})), raw=resp)


def normalize_embedding_response(resp: Any) -> NormalizedEmbeddingResponse:
    data = resp.data[0]
    return NormalizedEmbeddingResponse(model=getattr(resp, "model", None), vector=list(data.embedding), raw=resp)
