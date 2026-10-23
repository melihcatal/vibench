import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


DEFAULT_MODEL_FAMILY = "gpt-4o-mini"


def _env(key: str) -> Optional[str]:
    value = os.environ.get(key)
    return value if value else None


def _normalize_family_name(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    if name.startswith("gpt-4o"):
        return "gpt-4o"
    if name.startswith("gpt-4.1"):
        return "gpt-4.1"
    if name.startswith("gpt-3.5"):
        return "gpt-3.5"
    return name


@dataclass(frozen=True)
class ModelRequest:
    prompt: str
    model: Optional[str] = None
    family: Optional[str] = None
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NormalizedModelRequest:
    prompt: str
    model: str
    family: str
    temperature: Optional[float]
    max_output_tokens: Optional[int]
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class ModelResponse:
    text: str
    model: str
    family: str
    raw: Any = None


def load_model_defaults() -> Dict[str, Optional[str]]:
    return {
        "model": _env("OPENAI_MODEL"),
        "family": _env("OPENAI_MODEL_FAMILY"),
    }


def resolve_model_name(model: Optional[str] = None, family: Optional[str] = None) -> str:
    defaults = load_model_defaults()
    if model:
        return model
    if defaults["model"]:
        return defaults["model"] or DEFAULT_MODEL_FAMILY
    if family:
        return family
    if defaults["family"]:
        return defaults["family"] or DEFAULT_MODEL_FAMILY
    return DEFAULT_MODEL_FAMILY


def normalize_model_family(model: Optional[str] = None, family: Optional[str] = None) -> str:
    resolved = resolve_model_name(model=model, family=family)
    return _normalize_family_name(resolved) or DEFAULT_MODEL_FAMILY


def normalize_request(request: ModelRequest) -> NormalizedModelRequest:
    resolved_model = resolve_model_name(model=request.model, family=request.family)
    resolved_family = normalize_model_family(model=request.model, family=request.family)
    return NormalizedModelRequest(
        prompt=request.prompt,
        model=resolved_model,
        family=resolved_family,
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
        metadata=dict(request.metadata),
    )


def build_response(text: str, model: Optional[str] = None, family: Optional[str] = None, raw: Any = None) -> ModelResponse:
    resolved_model = resolve_model_name(model=model, family=family)
    resolved_family = normalize_model_family(model=model, family=family)
    return ModelResponse(text=text, model=resolved_model, family=resolved_family, raw=raw)


def request_to_chat_messages(request: ModelRequest) -> List[Dict[str, str]]:
    normalized = normalize_request(request)
    return [{"role": "user", "content": normalized.prompt}]
