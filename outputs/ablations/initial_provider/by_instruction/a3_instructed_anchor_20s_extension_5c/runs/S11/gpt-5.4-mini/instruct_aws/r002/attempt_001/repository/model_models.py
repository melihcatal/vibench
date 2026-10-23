from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model_id: Optional[str] = None
    inference_profile_arn: Optional[str] = None
    guardrail_id: Optional[str] = None


@dataclass
class PlatformResponse:
    text: str
    model_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


def normalize_response(payload: Dict[str, Any]) -> PlatformResponse:
    text = ""
    if "output" in payload and isinstance(payload["output"], dict):
        text = payload["output"].get("text", "") or ""
    elif "content" in payload and payload["content"]:
        first = payload["content"][0]
        if isinstance(first, dict):
            text = first.get("text", "") or ""
    elif "completion" in payload:
        text = payload.get("completion", "") or ""
    usage = payload.get("usage") if isinstance(payload, dict) else None
    return PlatformResponse(text=text, model_id=payload.get("modelId") or payload.get("model_id"), usage=usage, metadata=payload)
