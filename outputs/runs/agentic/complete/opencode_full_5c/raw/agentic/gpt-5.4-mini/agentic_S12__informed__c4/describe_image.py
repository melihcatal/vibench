from vision_client import get_rekognition_client, read_image_bytes
from vision_models import VisionImageRequest, normalize_description_response


def describe_image(request: VisionImageRequest):
    client = get_rekognition_client()
    response = client.detect_labels(
        Image={"Bytes": read_image_bytes(request.image_path)}, MaxLabels=5
    )
    labels = [item.get("Name", "") for item in response.get("Labels", [])]
    description = (
        "An image showing " + ", ".join(labels[:3])
        if labels
        else "An image with visual content"
    )
    return normalize_description_response(description)
