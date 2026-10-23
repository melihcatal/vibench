from __future__ import annotations

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import create_client
from vision_models import VisionResponse, normalize_text


def detect_image_text(image_path: str, image_url: str | None = None) -> VisionResponse:
    client = create_client()
    source = image_url or image_path
    result = client.analyze(source, visual_features=[VisualFeatures.READ])
    text_blocks = normalize_text(getattr(result, "read", []) or [])
    return VisionResponse(provider="Azure AI Vision", raw=result, text_blocks=text_blocks)
