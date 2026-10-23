from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


TextPart = Dict[str, Any]
MessageContent = Union[str, Sequence[TextPart]]


def _normalize_text_content(content: MessageContent) -> str:
    if isinstance(content, str):
        return content
    parts: List[str] = []
    for item in content:
        if isinstance(item, dict):
            text = item.get("text")
            if isinstance(text, str):
                parts.append(text)
        else:
            parts.append(str(item))
    return "".join(parts)


@dataclass(frozen=True)
class ModelRequest:
    model: Optional[str] = None
    family: Optional[str] = None
    input: Optional[MessageContent] = None
    messages: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def normalized_input(self) -> str:
        if self.input is not None:
            return _normalize_text_content(self.input)
        if self.messages:
            chunks: List[str] = []
            for message in self.messages:
                role = message.get("role", "")
                content = message.get("content", "")
                chunks.append(f"{role}: {_normalize_text_content(content)}")
            return "\n".join(chunks)
        return ""


@dataclass(frozen=True)
class ModelResponse:
    model: Optional[str] = None
    family: Optional[str] = None
    output_text: str = ""
    raw: Any = None
    usage: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)


def normalize_model_name(model: Optional[str] = None, family: Optional[str] = None, default_model: str = "gpt-5.4-mini") -> str:
    if model:
        return model
    if family == "gpt-5":
        return "gpt-5.4-mini"
    if family == "gpt-4.1":
        return "gpt-4.1-mini"
    return default_model


def normalize_response(raw: Any, model: Optional[str] = None, family: Optional[str] = None) -> ModelResponse:
    output_text = getattr(raw, "output_text", "") or ""
    usage = getattr(raw, "usage", {}) or {}
    return ModelResponse(model=model, family=family, output_text=output_text, raw=raw, usage=usage)
