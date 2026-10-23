from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import get_vision_client
from vision_models import normalize_description, ImageDescription


def describe_image(image_url: str) -> ImageDescription:
    client = get_vision_client()
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.CAPTION, VisualFeatures.TAGS],
    )
    raw_caption = {"text": "", "confidence": 0.0, "tags": []}
    if result.caption is not None:
        raw_caption["text"] = result.caption.text
        raw_caption["confidence"] = result.caption.confidence
    if result.tags is not None:
        raw_caption["tags"] = [tag.name for tag in result.tags.list]
    description = normalize_description(raw_caption)
    return description
