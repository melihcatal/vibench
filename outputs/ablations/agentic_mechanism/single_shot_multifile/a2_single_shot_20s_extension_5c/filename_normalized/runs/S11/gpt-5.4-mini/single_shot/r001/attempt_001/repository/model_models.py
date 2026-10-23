from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


def normalize_platform_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


@dataclass
class PlatformRequest:
    prompt: str
    system_instruction: Optional[str] = None
    temperature: float = 0.2
    max_output_tokens: int = 512

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PlatformResourceSelection:
    query: str
    model_id: str
    resource_name: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PlatformResponseBundle:
    text: str
    model_id: str
    usage: Dict[str, Any]
    raw_response: Any

    @classmethod
    def from_google_response(cls, response, model_id: str):
        usage = {}
        if hasattr(response, "usage_metadata") and response.usage_metadata is not None:
            usage = {
                "prompt_token_count": getattr(response.usage_metadata, "prompt_token_count", None),
                "candidates_token_count": getattr(response.usage_metadata, "candidates_token_count", None),
                "total_token_count": getattr(response.usage_metadata, "total_token_count", None),
            }
        text = response.text if hasattr(response, "text") else str(response)
        return cls(text=text, model_id=model_id, usage=usage, raw_response=response)

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "model_id": self.model_id, "usage": self.usage, "raw_response": self.raw_response}
