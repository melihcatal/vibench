from google.cloud import vision

from vision_client import build_image, get_vision_client
from vision_models import image_bytes_from_payload, normalize_labels


def describe_image(payload, config=None):
    config = config or {}
    client = get_vision_client()
    response = client.label_detection(image=build_image(payload), max_results=int(config.get("max_labels", 5)))
    if response.error.message:
        raise RuntimeError(response.error.message)
    labels = normalize_labels(response.label_annotations)
    if not labels:
        return {"description": ""}
    top = labels[0]["name"]
    return {"description": f"An image featuring {top.lower()}.", "labels": labels}
