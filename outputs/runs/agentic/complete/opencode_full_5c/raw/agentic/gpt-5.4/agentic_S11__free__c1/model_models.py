from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    system: Optional[str] = None
    temperature: float = 0.2
    max_output_tokens: int = 256
    locale: str = "en"
    model_hint: Optional[str] = None


@dataclass
class PlatformResponse:
    text: str
    model: str
    resource_id: str
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Optional[Any] = None


@dataclass
class SafetyResult:
    flagged: bool
    categories: Dict[str, bool]
    provider_result: Any


def build_messages(request: PlatformRequest) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = []
    if request.system:
        messages.append({"role": "system", "content": request.system})
    messages.append({"role": "user", "content": request.prompt})
    return messages


def extract_text_from_response(response: Any) -> str:
    output = getattr(response, "output", []) or []
    chunks: List[str] = []
    for item in output:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                chunks.append(text)
    return "".join(chunks)


def usage_to_dict(response: Any) -> Dict[str, Any]:
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    if hasattr(usage, "__dict__"):
        return dict(usage.__dict__)
    if isinstance(usage, dict):
        return usage
    return {"value": usage}


def normalize_response(response: Any, resource_id: str) -> PlatformResponse:
    model = getattr(response, "model", resource_id)
    return PlatformResponse(
        text=extract_text_from_response(response),
        model=model,
        resource_id=resource_id,
        usage=usage_to_dict(response),
        raw=response,
    )
