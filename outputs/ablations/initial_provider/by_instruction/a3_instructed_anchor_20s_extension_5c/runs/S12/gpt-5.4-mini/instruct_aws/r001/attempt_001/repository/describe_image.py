from typing import Any, Dict

from vision_client import rekognition_client, load_image_bytes
from vision_models import ImageSource, normalize_detect_labels_response


def describe_image(image: ImageSource) -> Dict[str, Any]:
    client = rekognition_client()
    response = client.detect_labels(Image={"Bytes": load_image_bytes(image)}, MaxLabels=5)
    labels = normalize_detect_labels_response(response)["labels"]
    description = ", ".join(label["name"] for label in labels[:3] if label.get("name"))
    return {"description": description, "labels": labels}
