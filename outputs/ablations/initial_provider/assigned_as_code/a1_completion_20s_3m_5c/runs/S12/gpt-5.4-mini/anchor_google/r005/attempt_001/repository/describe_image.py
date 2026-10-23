from google.cloud import vision

from vision_client import get_google_vision_client


def describe_image(payload, config=None):
    config = config or {}
    client = get_google_vision_client()
    response = client.label_detection(
        image=vision.Image(content=payload["image_bytes"]),
        max_results=int(config.get("max_candidates", 5)),
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    labels = [label.description for label in response.label_annotations[:3]]
    return {"description": ", ".join(labels)}
