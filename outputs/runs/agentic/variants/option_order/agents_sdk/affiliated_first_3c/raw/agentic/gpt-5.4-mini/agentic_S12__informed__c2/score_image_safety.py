from __future__ import annotations

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import create_client
from vision_models import VisionResponse, normalize_safety


def score_image_safety(image_path: str, image_url: str | None = None) -> VisionResponse:
    client = create_client()
    source = image_url or image_path
    result = client.analyze(source, visual_features=[VisualFeatures.OBJECTS, VisualFeatures.TAGS])
    safety_items = []
    for item in (getattr(result, "tags", []) or []):
        data = getattr(item, "__dict__", {})
        label = str(data.get("name") or "")
        flagged = label.lower() in {"nudity", "violence", "gore", "weapon"}
        if flagged:
            data = {**data, "flagged": True, "score": float(data.get("confidence") or 0.9)}
            safety_items.append(data)
    safety = normalize_safety(safety_items)
    return VisionResponse(provider="Azure AI Vision", raw=result, safety=safety)
