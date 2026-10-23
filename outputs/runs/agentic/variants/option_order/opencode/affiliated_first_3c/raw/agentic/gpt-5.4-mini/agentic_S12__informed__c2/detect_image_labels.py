import os

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import get_azure_vision_client, load_image_input
from vision_models import LabelDetectionResult, normalize_strings


def detect_image_labels(
    image_path: str, image_url: str | None = None
) -> LabelDetectionResult:
    client = get_azure_vision_client()
    image = load_image_input(image_path, image_url)
    source = (
        {"image_url": image.image_url}
        if image.image_url
        else {"image_data": open(image.image_path, "rb").read()}
    )
    result = client.analyze(
        **source, visual_features=[VisualFeatures.CAPTION, VisualFeatures.TAGS]
    )
    labels = []
    if getattr(result, "tags", None):
        labels.extend(normalize_strings([t.name for t in result.tags]))
    if getattr(result, "caption", None) and getattr(result.caption, "text", None):
        labels.append(result.caption.text)
    return LabelDetectionResult(
        labels=labels,
        raw=result.as_dict() if hasattr(result, "as_dict") else {"result": str(result)},
    )


__all__ = ["detect_image_labels"]
