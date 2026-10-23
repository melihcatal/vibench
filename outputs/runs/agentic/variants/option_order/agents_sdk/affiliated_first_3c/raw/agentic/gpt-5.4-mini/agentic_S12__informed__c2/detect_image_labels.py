from __future__ import annotations

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import create_client
from vision_models import ImageAnalysisRequest, VisionResponse, normalize_labels


def detect_image_labels(image_path: str, image_url: str | None = None) -> VisionResponse:
    client = create_client()
    request = ImageAnalysisRequest(image_path=image_path, image_url=image_url)
    source = image_url or image_path
    result = client.analyze(source, visual_features=[VisualFeatures.TAGS])
    labels = normalize_labels(getattr(result, "tags", []) or [])
    return VisionResponse(provider="Azure AI Vision", raw=result, labels=labels)
