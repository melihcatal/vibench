from __future__ import annotations

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_client, read_image_bytes, extract_safety


def score_image_safety(image_path: str):
    client = build_client()
    image = read_image_bytes(image_path)
    result = client.analyze(image_data=image, visual_features=[VisualFeatures.OBJECTS, VisualFeatures.TAGS])
    return extract_safety(result)
