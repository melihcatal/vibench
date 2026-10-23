from vision_client import get_vision_client
from vision_models import normalize_summary


def image_summary(payload, config=None):
    client = get_vision_client(config)
    labels_response = client.detect_labels(
        Image={"Bytes": payload["image_bytes"]},
        MaxLabels=10,
    )
    labels = [label["Name"] for label in labels_response["Labels"]]
    text_response = client.detect_text(
        Image={"Bytes": payload["image_bytes"]},
    )
    text = [detection["DetectedText"] for detection in text_response["TextDetections"]]
    return normalize_summary(labels, text)