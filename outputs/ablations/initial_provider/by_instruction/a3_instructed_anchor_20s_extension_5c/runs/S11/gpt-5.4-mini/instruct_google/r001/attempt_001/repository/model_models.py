from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ModelRequest:
    prompt: str
    model: Optional[str] = None
    temperature: Optional[float] = None


@dataclass
class ModelResponse:
    text: str
    metadata: Dict[str, Any]


def normalize_text(response: Any) -> str:
    if hasattr(response, "text") and response.text:
        return response.text
    parts = []
    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        if content and getattr(content, "parts", None):
            for part in content.parts:
                if hasattr(part, "text") and part.text:
                    parts.append(part.text)
    return "".join(parts)


def extract_metadata(response: Any) -> Dict[str, Any]:
    usage = getattr(response, "usage_metadata", None)
    metadata = {}
    if usage is not None:
        metadata["usage"] = {
            "prompt_tokens": getattr(usage, "prompt_token_count", None),
            "completion_tokens": getattr(usage, "candidates_token_count", None),
            "total_tokens": getattr(usage, "total_token_count", None),
        }
    metadata["model"] = getattr(response, "model_version", None) or getattr(response, "model", None)
    metadata["response_id"] = getattr(response, "response_id", None)
    return metadata
