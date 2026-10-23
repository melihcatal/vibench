from __future__ import annotations

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_client, read_image_bytes, extract_labels


def detect_image_labels(image_path: str, max_results: int = 10):
    client = build_client()
    image = read_image_bytes(image_path)
    result = client.analyze(image_data=image, visual_features=[VisualFeatures.TAGS])
    labels = extract_labels(result)
    return labels[:max_results]
