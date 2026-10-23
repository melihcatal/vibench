from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_client


def describe_image(image_path: str) -> str:
    client = build_client()
    with open(image_path, "rb") as f:
        result = client.analyze(data=f.read(), visual_features=[VisualFeatures.CAPTION])
    caption = getattr(result, "caption", None)
    if caption and getattr(caption, "text", None):
        return str(caption.text)
    return ""
