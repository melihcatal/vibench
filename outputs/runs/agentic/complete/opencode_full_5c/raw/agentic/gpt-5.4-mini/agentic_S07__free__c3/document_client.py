import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import vision


@dataclass
class DocumentClientConfig:
    project_id: Optional[str] = None
    location: Optional[str] = None
    language_hints: Optional[list[str]] = None


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        language_hints=[
            h for h in (os.getenv("OCR_LANGUAGE_HINTS") or "").split(",") if h
        ],
    )


def vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def normalize_image_source(image_source: Any) -> Dict[str, Any]:
    if isinstance(image_source, bytes):
        return {"content": image_source}
    if isinstance(image_source, str):
        return (
            {"uri": image_source}
            if image_source.startswith("gs://") or image_source.startswith("http")
            else {"path": image_source}
        )
    if isinstance(image_source, dict):
        return image_source
    raise TypeError("Unsupported image source")
