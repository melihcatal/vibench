from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class PlatformInvocationRequest:
    prompt: str
    resource_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformResourceSelection:
    provider: str
    resource_id: str
    model_id: str
    deployment_id: Optional[str] = None


@dataclass
class PlatformStreamChunk:
    provider: str
    raw: Any
    text: str

    def to_dict(self) -> Dict[str, Any]:
        return {"provider": self.provider, "text": self.text, "raw": self.raw}



def coerce_text(response: Any) -> str:
    if response is None:
        return ""
    if isinstance(response, str):
        return response
    for attr in ("output_text", "text"):
        value = getattr(response, attr, None)
        if isinstance(value, str):
            return value
    content = getattr(response, "content", None)
    if isinstance(content, list):
        parts = []
        for item in content:
            text = getattr(item, "text", None) or getattr(item, "input_text", None)
            if isinstance(text, str):
                parts.append(text)
        if parts:
            return "".join(parts)
    return str(response)



def collect_usage(response: Any) -> Dict[str, Any]:
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    if isinstance(usage, dict):
        return usage
    result = {}
    for key in ("input_tokens", "output_tokens", "total_tokens", "prompt_tokens", "completion_tokens"):
        value = getattr(usage, key, None)
        if value is not None:
            result[key] = value
    return result
