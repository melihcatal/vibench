from vision_client import get_rekognition_client, read_image_bytes
from vision_models import VisionSafetyRequest, normalize_safety_response


def score_image_safety(request: VisionSafetyRequest):
    client = get_rekognition_client()
    response = client.detect_moderation_labels(
        Image={"Bytes": read_image_bytes(request.image_path)}
    )
    labels = [item.get("Name", "") for item in response.get("ModerationLabels", [])]
    return normalize_safety_response({"unsafe": bool(labels), "labels": labels})
