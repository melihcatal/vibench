from google.cloud import vision


def describe_image(payload, config=None):
    config = config or {}
    client = vision.ImageAnnotatorClient()
    response = client.label_detection(
        image=vision.Image(content=payload["image_bytes"]),
        max_results=int(config.get("max_labels", 10)),
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    return {"description": " ".join([label.description for label in response.label_annotations])}