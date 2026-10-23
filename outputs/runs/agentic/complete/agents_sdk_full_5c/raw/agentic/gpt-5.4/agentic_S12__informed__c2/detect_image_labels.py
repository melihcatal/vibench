from __future__ import annotations

from typing import Dict, Any

from vision_client import VisionClientFactory, build_vision_image, GOOGLE_VISION_MODEL, GOOGLE_VISION_PROVIDER
from vision_models import ImageSource, LabelDetection, VisionResult, normalize_confidence


def detect_image_labels(source: ImageSource, max_results: int = 15) -> Dict[str, Any]:
    client = VisionClientFactory.create_image_annotator_client()
    image = build_vision_image(source)
    response = client.label_detection(image=image, max_results=max_results)
    labels = [
        LabelDetection(
            name=annotation.description,
            confidence=normalize_confidence(annotation.score),
            categories=[],
        )
        for annotation in response.label_annotations
    ]
    result = VisionResult(
        provider=GOOGLE_VISION_PROVIDER,
        model=GOOGLE_VISION_MODEL,
        labels=labels,
        raw_response={"label_count": len(response.label_annotations)},
    )
    return result.to_dict()
