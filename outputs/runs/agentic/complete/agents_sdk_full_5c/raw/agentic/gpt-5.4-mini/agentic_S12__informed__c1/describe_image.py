from __future__ import annotations

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_client, read_image_bytes, extract_description


def describe_image(image_path: str) -> str:
    client = build_client()
    image = read_image_bytes(image_path)
    result = client.analyze(image_data=image, visual_features=[VisualFeatures.CAPTION])
    description = extract_description(result)
    return description.caption
