from __future__ import annotations

from google.cloud import vision

from vision_client import build_vision_image, get_google_vision_client
from vision_models import ImageDescriptionResult


GOOGLE_VISION_FEATURE = vision.Feature.Type.OBJECT_LOCALIZATION


def describe_image(image_path: str, max_objects: int = 5) -> ImageDescriptionResult:
    client = get_google_vision_client()
    image = build_vision_image(image_path)
    response = client.object_localization(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    objects = sorted(response.localized_object_annotations, key=lambda x: x.score, reverse=True)
    top = objects[:max_objects]
    if not top:
        return ImageDescriptionResult(text="No prominent visual objects detected.", confidence=0.0)
    parts = [obj.name.lower() for obj in top]
    confidence = sum(float(obj.score) for obj in top) / len(top)
    text = "Image may contain " + ", ".join(parts[:-1] + [parts[-1]]) + "."
    return ImageDescriptionResult(text=text, confidence=confidence)
