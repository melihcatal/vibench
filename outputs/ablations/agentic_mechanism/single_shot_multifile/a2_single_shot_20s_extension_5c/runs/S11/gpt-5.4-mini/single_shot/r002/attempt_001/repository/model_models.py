from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class GenerationInput:
    prompt: str
    model: Optional[str] = None
    temperature: float = 0.2
    max_output_tokens: int = 512


@dataclass
class ResourceSelection:
    prompt: str
    model: Optional[str] = None
    scope: Optional[str] = None


@dataclass
class ModelResponse:
    output: str
    provider: str
    model: str
    request_id: Optional[str]
    usage: Any
    raw: Any


@dataclass
class PlatformResource:
    provider: str
    resource_id: str
    model: str
    metadata: Dict[str, Any]


@dataclass
class StreamChunk:
    provider: str
    model: str
    text: str
    raw: Any


@dataclass
class MetadataBundle:
    output: str
    provider: str
    model: str
    request_id: Optional[str]
    usage: Any
    raw: Any


def normalize_generation_input(request: Dict[str, Any] | GenerationInput) -> GenerationInput:
    if isinstance(request, GenerationInput):
        return request
    return GenerationInput(
        prompt=request.get("prompt", ""),
        model=request.get("model"),
        temperature=float(request.get("temperature", 0.2)),
        max_output_tokens=int(request.get("max_output_tokens", 512)),
    )


def normalize_resource_selection(request: Dict[str, Any] | ResourceSelection) -> ResourceSelection:
    if isinstance(request, ResourceSelection):
        return request
    return ResourceSelection(
        prompt=request.get("prompt", ""),
        model=request.get("model"),
        scope=request.get("scope"),
    )


def normalize_text_output(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if text:
        return text
    output = getattr(response, "output", None)
    if isinstance(output, list):
        parts = []
        for item in output:
            content = getattr(item, "content", None)
            if isinstance(content, list):
                for c in content:
                    value = getattr(c, "text", None)
                    if value:
                        parts.append(value)
        if parts:
            return "".join(parts)
    return str(response)


def normalize_stream_chunk(event: Any, provider: str, model: str) -> StreamChunk:
    text = getattr(event, "delta", None) or getattr(event, "text", None) or str(event)
    return StreamChunk(provider=provider, model=model, text=text, raw=event)
