from __future__ import annotations

from typing import Optional

from vision_client import (
    build_image_source,
    get_google_vision_client,
    image_source_to_google_image,
)
from vision_models import (
    ImageLabelsResult,
    LabelDetection,
    labels_result_dict,
    normalize_score,
)


def detect_image_labels(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    max_results: int = 10,
) -> dict:
    image = build_image_source(image_path=image_path, image_uri=image_uri)
    client = get_google_vision_client()
    response = client.label_detection(
        image=image_source_to_google_image(image), max_results=max_results
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    result = ImageLabelsResult(
        provider="google-cloud-vision",
        labels=[
            LabelDetection(
                name=annotation.description, score=normalize_score(annotation.score)
            )
            for annotation in response.label_annotations
        ],
    )
    return labels_result_dict(result)
