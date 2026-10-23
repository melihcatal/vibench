from __future__ import annotations

from typing import Dict, Any

from vision_client import VisionClientFactory, build_vision_image, GOOGLE_VISION_MODEL, GOOGLE_VISION_PROVIDER
from vision_models import ImageSource, VisionResult, normalize_confidence


def describe_image(source: ImageSource) -> Dict[str, Any]:
    client = VisionClientFactory.create_image_annotator_client()
    image = build_vision_image(source)
    response = client.label_detection(image=image, max_results=8)
    best = sorted(response.label_annotations, key=lambda item: item.score, reverse=True)
    confident = [item.description for item in best if normalize_confidence(item.score) >= 0.6][:3]
    if confident:
        description = "Image showing " + ", ".join(confident) + "."
    elif best:
        description = f"Image likely contains {best[0].description}."
    else:
        description = "No clear visual description could be generated."
    result = VisionResult(
        provider=GOOGLE_VISION_PROVIDER,
        model=GOOGLE_VISION_MODEL,
        description=description,
        raw_response={"source": "google.cloud.vision.label_detection"},
    )
    return result.to_dict()
