from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_client
from vision_models import normalize_strings


def detect_image_labels(image_path: str):
    client = build_client()
    with open(image_path, "rb") as f:
        result = client.analyze(data=f.read(), visual_features=[VisualFeatures.TAGS])
    labels = []
    for tag in getattr(result, "tags", []) or []:
        if getattr(tag, "name", None):
            labels.append(tag.name)
    return normalize_strings(labels)
