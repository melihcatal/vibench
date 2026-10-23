from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_client
from vision_models import normalize_strings


def detect_image_text(image_path: str):
    client = build_client()
    with open(image_path, "rb") as f:
        result = client.analyze(data=f.read(), visual_features=[VisualFeatures.READ])
    text = []
    for block in getattr(result, "read", []) or []:
        for line in getattr(block, "lines", []) or []:
            if getattr(line, "text", None):
                text.append(line.text)
    return normalize_strings(text)
