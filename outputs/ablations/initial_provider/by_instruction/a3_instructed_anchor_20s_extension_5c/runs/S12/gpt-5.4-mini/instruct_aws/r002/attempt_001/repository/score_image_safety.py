from vision_client import image_bytes, rekognition_client
from vision_models import normalize_safety


def score_image_safety(source):
    client = rekognition_client()
    response = client.detect_moderation_labels(Image={"Bytes": image_bytes(source)})
    return normalize_safety(response.get("ModerationLabels"))
