from vision_client import image_bytes, rekognition_client
from vision_models import normalize_labels


def detect_image_labels(source, max_labels=10, min_confidence=50):
    client = rekognition_client()
    response = client.detect_labels(
        Image={"Bytes": image_bytes(source)},
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )
    return normalize_labels(response.get("Labels"))
