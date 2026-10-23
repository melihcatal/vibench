from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class StaticImageRequest:
    image_path: str
    prompt: str = "Describe this image."


@dataclass
class VisualUnderstandingRequest:
    image_path: str
    prompt: str


@dataclass
class VisionResponse:
    text: str
    raw: Optional[Dict[str, Any]] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = [normalize_text(item) for item in value]
        return "\n".join(part for part in parts if part)
    if isinstance(value, dict):
        for key in ("text", "content", "output_text", "answer", "description"):
            normalized = normalize_text(value.get(key))
            if normalized:
                return normalized
    return str(value).strip()


def normalize_static_image_response(response: Any) -> VisionResponse:
    if isinstance(response, dict):
        return VisionResponse(text=normalize_text(response), raw=response)
    return VisionResponse(text=normalize_text(response))


def normalize_visual_understanding_response(response: Any) -> VisionResponse:
    return normalize_static_image_response(response)


def build_static_image_request(image_path: str, prompt: str = "Describe this image.") -> StaticImageRequest:
    return StaticImageRequest(image_path=image_path, prompt=prompt)


def build_visual_understanding_request(image_path: str, prompt: str) -> VisualUnderstandingRequest:
    return VisualUnderstandingRequest(image_path=image_path, prompt=prompt)


def serialize_request(request: Any) -> Dict[str, Any]:
    return {k: v for k, v in request.__dict__.items() if v is not None}


def response_to_text(response: Any) -> str:
    if isinstance(response, VisionResponse):
        return response.text
    return normalize_text(response)
