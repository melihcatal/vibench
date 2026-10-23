from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def normalize_platform_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        return text if text else None
    text = getattr(value, "text", None)
    if isinstance(text, str):
        stripped = text.strip()
        return stripped if stripped else None
    return str(value)


def normalize_platform_metadata(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "model_dump"):
        dumped = value.model_dump()
        return dumped if isinstance(dumped, dict) else {"value": dumped}
    if hasattr(value, "to_dict"):
        dumped = value.to_dict()
        return dumped if isinstance(dumped, dict) else {"value": dumped}
    if hasattr(value, "__dict__"):
        return {
            key: item
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    return {"value": value}


@dataclass
class ManagedModelPlatformRequest:
    prompt: str
    model: Optional[str] = None
    system_instruction: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    request_kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ManagedModelPlatformResponse:
    text: Optional[str]
    response: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_managed_model_request(request: Any) -> ManagedModelPlatformRequest:
    if isinstance(request, ManagedModelPlatformRequest):
        return request
    if isinstance(request, dict):
        return ManagedModelPlatformRequest(
            prompt=str(request.get("prompt", "")),
            model=request.get("model"),
            system_instruction=request.get("system_instruction"),
            metadata=normalize_platform_metadata(request.get("metadata")),
            request_kwargs=normalize_platform_metadata(
                request.get("request_kwargs")
            ),
        )
    prompt = normalize_platform_text(getattr(request, "prompt", None)) or ""
    return ManagedModelPlatformRequest(
        prompt=prompt,
        model=getattr(request, "model", None),
        system_instruction=getattr(request, "system_instruction", None),
        metadata=normalize_platform_metadata(getattr(request, "metadata", None)),
        request_kwargs=normalize_platform_metadata(
            getattr(request, "request_kwargs", None)
        ),
    )


def normalize_managed_model_response(response: Any) -> ManagedModelPlatformResponse:
    if isinstance(response, ManagedModelPlatformResponse):
        return response
    if isinstance(response, dict):
        return ManagedModelPlatformResponse(
            text=normalize_platform_text(response.get("text")),
            response=response.get("response"),
            metadata=normalize_platform_metadata(response.get("metadata")),
        )
    return ManagedModelPlatformResponse(
        text=normalize_platform_text(response),
        response=response,
        metadata=normalize_platform_metadata(getattr(response, "metadata", None)),
    )
