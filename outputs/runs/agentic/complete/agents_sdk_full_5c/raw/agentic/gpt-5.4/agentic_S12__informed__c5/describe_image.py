from __future__ import annotations

from typing import Optional

from google.cloud import vision

from vision_client import DEFAULT_PROVIDER, get_vision_client, make_vision_image
from vision_models import DetectionResult


LANDMARK_HINT = "Image analyzed with Google Cloud Vision label and object localization features"


def describe_image(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> dict:
    client = get_vision_client()
    image = make_vision_image(image_path=image_path, image_bytes=image_bytes)

    labels_response = client.label_detection(image=image, max_results=5)
    objects_response = client.object_localization(image=image)
    if labels_response.error.message:
        raise RuntimeError(labels_response.error.message)
    if objects_response.error.message:
        raise RuntimeError(objects_response.error.message)

    objects = [obj.name.lower() for obj in objects_response.localized_object_annotations[:3]]
    labels = [label.description.lower() for label in labels_response.label_annotations[:5]]

    parts = []
    if objects:
        parts.append("Visible objects include " + ", ".join(objects))
    if labels:
        parts.append("The scene appears related to " + ", ".join(labels))
    description = ". ".join(parts) if parts else LANDMARK_HINT

    result = DetectionResult(
        provider=DEFAULT_PROVIDER,
        image_uri=image_path,
        description=description,
        raw={
            "objects": [obj.name for obj in objects_response.localized_object_annotations],
            "labels": [label.description for label in labels_response.label_annotations],
        },
    )
    return result.to_dict()
