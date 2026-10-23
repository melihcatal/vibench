from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


OPENAI_VISION_MODEL = "gpt-4o-mini"


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_string_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        lines = [line.strip("-• \t") for line in value.splitlines()]
        return [line for line in lines if line]
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        return [normalize_text(item) for item in value if normalize_text(item)]
    return [normalize_text(value)] if normalize_text(value) else []


def normalize_labels(value: Any) -> List[str]:
    return normalize_string_list(value)


def normalize_description(value: Any) -> str:
    return normalize_text(value)


def normalize_confidence(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        score = float(value)
    except (TypeError, ValueError):
        return None
    return max(0.0, min(1.0, score))


@dataclass(frozen=True)
class VisionRequest:
    image_path: str
    prompt: str
    model: str = OPENAI_VISION_MODEL
    max_tokens: int = 128
    temperature: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self, image_url: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": [{"type": "text", "text": self.prompt}]}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if image_url is not None:
            payload["messages"][0]["content"].append({"type": "image_url", "image_url": {"url": image_url}})
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class VisionResponse:
    content: str = ""
    labels: List[str] = field(default_factory=list)
    description: str = ""
    safety_label: str = ""
    confidence: Optional[float] = None
    raw: Optional[Mapping[str, Any]] = None

    @classmethod
    def from_api_response(cls, data: Mapping[str, Any]) -> "VisionResponse":
        choices = data.get("choices") if isinstance(data, Mapping) else None
        content = ""
        if isinstance(choices, list) and choices:
            message = choices[0].get("message", {}) if isinstance(choices[0], Mapping) else {}
            content = normalize_text(message.get("content"))
        output_text = normalize_text(data.get("output_text")) if isinstance(data, Mapping) else ""
        text = content or output_text
        labels = normalize_labels(data.get("labels") if isinstance(data, Mapping) else None)
        description = normalize_description(data.get("description") if isinstance(data, Mapping) else None) or text
        safety_label = normalize_text(data.get("safety_label") if isinstance(data, Mapping) else None)
        confidence = normalize_confidence(data.get("confidence") if isinstance(data, Mapping) else None)
        return cls(content=text, labels=labels, description=description, safety_label=safety_label, confidence=confidence, raw=data)


def normalize_visual_analysis(data: Mapping[str, Any]) -> Dict[str, Any]:
    response = VisionResponse.from_api_response(data)
    return {
        "content": response.content,
        "labels": response.labels,
        "description": response.description,
        "safety_label": response.safety_label,
        "confidence": response.confidence,
    }
