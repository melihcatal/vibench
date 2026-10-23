from vision_client import get_rekognition_client, read_image_bytes
from vision_models import VisionImageRequest, normalize_label_response


def detect_image_labels(request: VisionImageRequest):
    client = get_rekognition_client()
    response = client.detect_labels(
        Image={"Bytes": read_image_bytes(request.image_path)}
    )
    labels = [item.get("Name", "") for item in response.get("Labels", [])]
    return normalize_label_response(
        labels[: request.max_results] if request.max_results else labels
    )
