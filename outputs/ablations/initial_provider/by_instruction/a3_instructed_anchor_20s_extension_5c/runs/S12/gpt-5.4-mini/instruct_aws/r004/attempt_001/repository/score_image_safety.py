from vision_client import load_image_input, rekognition_client
from vision_models import VisionResult, normalize_safety


def score_image_safety(image_path: str) -> VisionResult:
    image = load_image_input(image_path)
    client = rekognition_client()
    response = client.detect_moderation_labels(Image={"Bytes": image.image_bytes})
    labels = normalize_safety(
        [
            {
                "name": item.get("Name"),
                "parent_name": item.get("ParentName"),
                "confidence": float(item.get("Confidence", 0.0)),
            }
            for item in response.get("ModerationLabels", [])
        ]
    )
    unsafe = any(label.get("confidence", 0.0) >= 50.0 for label in labels)
    return VisionResult(provider="aws.rekognition", kind="safety", source=image.image_path, data={"unsafe": unsafe, "labels": labels})
