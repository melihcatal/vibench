from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    system_prompt: Optional[str] = None
    max_output_tokens: int = 256
    temperature: float = 0.2
    locale: str = "en"
    resource_id: Optional[str] = None


@dataclass
class PlatformResponse:
    text: str
    model: str
    resource_id: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    provider_response: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def build_messages(request: PlatformRequest) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = []
    if request.system_prompt:
        messages.append({"role": "system", "content": request.system_prompt})
    messages.append({"role": "user", "content": request.prompt})
    return messages


def usage_to_dict(usage: Any) -> Dict[str, Any]:
    if usage is None:
        return {}
    if isinstance(usage, dict):
        return usage
    if hasattr(usage, "model_dump"):
        return usage.model_dump()
    if hasattr(usage, "dict"):
        return usage.dict()
    return {
        key: getattr(usage, key)
        for key in dir(usage)
        if not key.startswith("_") and not callable(getattr(usage, key))
    }


def extract_text_from_response(response: Any) -> str:
    if response is None:
        return ""
    output = getattr(response, "output", None)
    if output:
        parts: List[str] = []
        for item in output:
            content = getattr(item, "content", None)
            if not content:
                continue
            for block in content:
                text = getattr(block, "text", None)
                if text:
                    parts.append(text)
        if parts:
            return "".join(parts)
    if hasattr(response, "output_text"):
        return response.output_text or ""
    return ""
