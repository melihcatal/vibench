from __future__ import annotations

from google.cloud import vision

from vision_client import get_client, make_image
from vision_models import DescriptionResult, ImageRequest


def describe_image(image_path: str, language: str = "en"):
    request = ImageRequest(image_path=image_path, language=language)
    client = get_client()
    image = make_image(request.image_path)
    response = client.image_properties(image=image)
    if response and response.image_properties_annotation:
        dominant = response.image_properties_annotation.dominant_colors.colors[:1]
        if dominant:
            color = dominant[0]
            text = f"An image with prominent {color.color.red:.0f}/{color.color.green:.0f}/{color.color.blue:.0f} tones."
            return DescriptionResult(text=text, confidence=float(color.score))
    # fallback to label-based captioning signal from Cloud Vision
    captions = client.annotate_image({"image": image, "features": [vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION)]})
    labels = captions.label_annotations if captions.label_annotations else []
    if labels:
        top = labels[0].description
        return DescriptionResult(text=f"A visual scene featuring {top}.", confidence=float(labels[0].score))
    return DescriptionResult(text="A visual scene.", confidence=0.0)
