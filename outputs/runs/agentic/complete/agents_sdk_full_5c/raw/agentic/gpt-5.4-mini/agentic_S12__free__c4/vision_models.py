from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ImageBaseRequest:
    image_url: str
    image_path: Optional[str] = None

    def load_bytes(self) -> bytes:
        if self.image_path:
            return Path(self.image_path).read_bytes()
        raise ValueError("image_path is required for binary image APIs")


@dataclass
class ImageAnalysisRequest(ImageBaseRequest):
    max_labels: int = 10


@dataclass
class ImageDescriptionRequest(ImageBaseRequest):
    max_tokens: int = 80

    def as_openai_content(self) -> List[Dict[str, Any]]:
        return [
            {"type": "input_text", "text": "Provide a short visual description of this image."},
            {"type": "input_image", "image_url": self.image_url},
        ]


@dataclass
class ImageTextRequest(ImageBaseRequest):
    pass


@dataclass
class ImageSafetyRequest(ImageBaseRequest):
    pass


def normalize_vision_label_results(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    labels = result.get("labels", [])
    return [{"label": item.get("name", ""), "confidence": float(item.get("confidence", 0.0))} for item in labels]


def normalize_description(response: Dict[str, Any]) -> str:
    return str(response.get("text", "")).strip()


def normalize_detected_text(response: Dict[str, Any]) -> List[str]:
    return [str(t).strip() for t in response.get("texts", []) if str(t).strip()]


def normalize_safety_score(response: Dict[str, Any]) -> Dict[str, Any]:
    labels = response.get("labels", [])
    return {"provider": response.get("provider", ""), "labels": labels, "unsafe": bool(labels)}
