from __future__ import annotations

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_client, read_image_bytes, extract_text


def detect_image_text(image_path: str):
    client = build_client()
    image = read_image_bytes(image_path)
    result = client.analyze(image_data=image, visual_features=[VisualFeatures.READ])
    return extract_text(result)
