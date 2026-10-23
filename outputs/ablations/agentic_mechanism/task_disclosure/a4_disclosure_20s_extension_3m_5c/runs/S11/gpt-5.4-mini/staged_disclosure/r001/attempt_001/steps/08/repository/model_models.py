import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence

from openai import OpenAI


@dataclass(frozen=True)
class ManagedModelRequest:
    prompt: str
    model: str = "gpt-4.1-mini"
    provider: str = "openai"
    max_output_tokens: int = 256
    temperature: Optional[float] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ManagedModelUsage:
    input_tokens: Optional[int]
    output_tokens: Optional[int]
    total_tokens: Optional[int]


@dataclass(frozen=True)
class ManagedModelResponse:
    provider: str
    model: str
    response_id: Optional[str]
    output_text: str
    usage: ManagedModelUsage
    raw: Mapping[str, Any]


def load_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    return OpenAI(api_key=api_key, base_url=base_url)


def normalize_request(data: Any) -> ManagedModelRequest:
    if isinstance(data, ManagedModelRequest):
        return data
    if isinstance(data, str):
        return ManagedModelRequest(prompt=data)
    if not isinstance(data, Mapping):
        raise TypeError("request must be a string, mapping, or ManagedModelRequest")
    prompt = str(data.get("prompt", ""))
    if not prompt:
        raise ValueError("prompt is required")
    return ManagedModelRequest(
        prompt=prompt,
        model=str(data.get("model", "gpt-4.1-mini")),
        provider=str(data.get("provider", "openai")),
        max_output_tokens=int(data.get("max_output_tokens", 256)),
        temperature=data.get("temperature"),
        metadata=dict(data.get("metadata", {})),
    )


def _extract_output_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text
    chunks: List[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            if getattr(content, "type", None) == "output_text":
                chunks.append(getattr(content, "text", ""))
    return "".join(chunks)


def normalize_response(response: Any, provider: str = "openai", model: Optional[str] = None) -> ManagedModelResponse:
    usage = getattr(response, "usage", None)
    model_name = model or getattr(response, "model", None) or ""
    return ManagedModelResponse(
        provider=provider,
        model=model_name,
        response_id=getattr(response, "id", None),
        output_text=_extract_output_text(response),
        usage=ManagedModelUsage(
            input_tokens=getattr(usage, "input_tokens", None) if usage else None,
            output_tokens=getattr(usage, "output_tokens", None) if usage else None,
            total_tokens=getattr(usage, "total_tokens", None) if usage else None,
        ),
        raw=response.model_dump() if hasattr(response, "model_dump") else dict(response),
    )


def build_openai_input(request: ManagedModelRequest) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"model": request.model, "input": request.prompt}
    if request.max_output_tokens is not None:
        payload["max_output_tokens"] = request.max_output_tokens
    if request.temperature is not None:
        payload["temperature"] = request.temperature
    if request.metadata:
        payload["metadata"] = dict(request.metadata)
    return payload


def invoke_managed_model(data: Any, client: Optional[OpenAI] = None) -> ManagedModelResponse:
    request = normalize_request(data)
    if request.provider != "openai":
        raise ValueError(f"unsupported provider: {request.provider}")
    api_client = client or load_openai_client()
    response = api_client.responses.create(**build_openai_input(request))
    return normalize_response(response, provider=request.provider, model=request.model)
