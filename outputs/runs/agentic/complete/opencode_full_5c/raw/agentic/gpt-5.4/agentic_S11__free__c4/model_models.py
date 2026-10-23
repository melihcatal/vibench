from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional


class PlatformRequest:
    def __init__(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
        locale: str = "en",
        voice: str = "alloy",
    ):
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.locale = locale
        self.voice = voice


class PlatformResponse:
    def __init__(
        self,
        text: str,
        model: str,
        resource_id: Optional[str] = None,
        usage: Optional[Dict[str, Any]] = None,
        raw: Optional[Any] = None,
    ):
        self.text = text
        self.model = model
        self.resource_id = resource_id
        self.usage = usage or {}
        self.raw = raw

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "model": self.model,
            "resource_id": self.resource_id,
            "usage": self.usage,
        }


def messages_from_prompt(prompt: str) -> List[Dict[str, str]]:
    return [{"role": "user", "content": prompt}]


def extract_text_from_response(response: Any) -> str:
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text
    output = getattr(response, "output", None) or []
    collected: List[str] = []
    for item in output:
        content = getattr(item, "content", None) or []
        for part in content:
            text = getattr(part, "text", None)
            if text:
                collected.append(text)
    return "".join(collected)


def extract_usage(response: Any) -> Dict[str, Any]:
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    if isinstance(usage, dict):
        return usage
    result: Dict[str, Any] = {}
    for field in ("input_tokens", "output_tokens", "total_tokens"):
        value = getattr(usage, field, None)
        if value is not None:
            result[field] = value
    return result


def normalize_stream_text(events: Iterable[Any]) -> str:
    parts: List[str] = []
    for event in events:
        if getattr(event, "type", "") == "response.output_text.delta":
            delta = getattr(event, "delta", None)
            if delta:
                parts.append(delta)
    return "".join(parts)
