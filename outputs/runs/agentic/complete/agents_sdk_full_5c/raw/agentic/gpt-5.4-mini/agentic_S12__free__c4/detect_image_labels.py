from __future__ import annotations

from typing import Any, Dict, List

from vision_client import get_azure_vision_analyzer
from vision_models import ImageAnalysisRequest, normalize_vision_label_results


def detect_image_labels(image_url: str, *, image_path: str | None = None, max_labels: int = 10) -> List[Dict[str, Any]]:
    """Detect labels/objects in a static image using Azure AI Vision."""
    request = ImageAnalysisRequest(image_url=image_url, image_path=image_path, max_labels=max_labels)
    client = get_azure_vision_analyzer()
    result = client.analyze_image(request)
    return normalize_vision_label_results(result)
