import boto3

from vision_models import normalize_safety_response


def score_image_safety(payload, config=None):
    config = config or {}
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_moderation_labels(Image={"Bytes": payload["image_bytes"]}, MinConfidence=float(config.get("min_confidence", 0)))
    categories = [{"name": label["Name"], "confidence": label["Confidence"] / 100.0} for label in response.get("ModerationLabels", [])]
    unsafe = any(item["confidence"] >= 0.5 for item in categories)
    summary = ", ".join(item["name"] for item in categories)
    return normalize_safety_response({"unsafe": unsafe, "categories": categories, "summary": summary})
