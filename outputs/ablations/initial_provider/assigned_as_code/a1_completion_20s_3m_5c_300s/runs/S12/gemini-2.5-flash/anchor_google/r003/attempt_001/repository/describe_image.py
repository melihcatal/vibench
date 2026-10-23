from google.cloud import vision
from vision_client import get_vision_client


def describe_image(payload, config=None):
    config = config or {}
    client = get_vision_client()
    response = client.label_detection(
        image=vision.Image(content=payload["image_bytes"]),
        max_results=int(config.get("max_labels_for_description", 5)),
    )
    if response.error.message:
        raise RuntimeError(response.error.message)

    labels = [label.description for label in response.label_annotations]
    if labels:
        return {"description": f"An image featuring: {', '.join(labels)}."}
    else:
        return {"description": "A scene without clear dominant features."}
