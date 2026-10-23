from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_client


def score_image_safety(image_path: str):
    client = build_client()
    with open(image_path, "rb") as f:
        result = client.analyze(data=f.read(), visual_features=[VisualFeatures.SMART_CROPS])
    categories = getattr(result, "moderation", None)
    unsafe = bool(getattr(categories, "is_adult_content", False) or getattr(categories, "is_racy_content", False))
    reasons = []
    if getattr(categories, "is_adult_content", False):
        reasons.append("adult_content")
    if getattr(categories, "is_racy_content", False):
        reasons.append("racy_content")
    return {"unsafe": unsafe, "reasons": reasons}
