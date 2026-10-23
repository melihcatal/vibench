from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model_id: Optional[str] = None
    messages: List[Dict[str, Any]] = field(default_factory=list)
    inference_config: Dict[str, Any] = field(default_factory=dict)
    system: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class PlatformResponse:
    text: str
    raw: Dict[str, Any]
    usage: Dict[str, Any] = field(default_factory=dict)
    resource_id: Optional[str] = None
    model_id: Optional[str] = None


def normalize_request(request: PlatformRequest) -> Dict[str, Any]:
    messages = request.messages or [{"role": "user", "content": [{"text": request.prompt}]}]
    return {"messages": messages, "inferenceConfig": request.inference_config, "system": request.system}


def extract_text(response: Dict[str, Any]) -> str:
    outputs = response.get("output", {}).get("message", {}).get("content", [])
    parts = []
    for item in outputs:
        if "text" in item:
            parts.append(item["text"])
    return "".join(parts)


def wrap_response(response: Dict[str, Any]) -> PlatformResponse:
    return PlatformResponse(
        text=extract_text(response),
        raw=response,
        usage=response.get("usage", {}),
        resource_id=response.get("ResponseMetadata", {}).get("RequestId"),
        model_id=response.get("modelId"),
    )
