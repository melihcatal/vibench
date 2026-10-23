from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PlatformRequest:
    prompt: str
    temperature: float = 0.2
    max_output_tokens: int = 256


@dataclass
class PlatformResponse:
    text: str
    metadata: Dict[str, Any]


def normalize_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload.strip()
    if isinstance(payload, dict):
        for key in ("text", "output_text", "content"):
            value = payload.get(key)
            if isinstance(value, str):
                return value.strip()
    return str(payload).strip()


def metadata_from_prediction(prediction: Any, model_name: str) -> Dict[str, Any]:
    return {"model_name": model_name, "prediction": prediction}
