from __future__ import annotations

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import create_client
from vision_models import VisionResponse


def describe_image(image_path: str, image_url: str | None = None) -> VisionResponse:
    client = create_client()
    source = image_url or image_path
    result = client.analyze(source, visual_features=[VisualFeatures.CAPTION])
    caption = getattr(getattr(result, "caption", None), "text", None)
    return VisionResponse(provider="Azure AI Vision", raw=result, summary=caption)
