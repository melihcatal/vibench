import os
from dataclasses import dataclass

from google.cloud import vision


@dataclass
class DocumentConfig:
    project_id: str | None = None
    location: str | None = None


def load_config() -> DocumentConfig:
    return DocumentConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION") or "us",
    )


def vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def image_from_content(content: bytes) -> vision.Image:
    return vision.Image(content=content)
