from google.cloud import vision

from vision_client import load_config


def describe_image(payload, config=None):
    cfg = load_config(config)
    client = vision.ImageAnnotatorClient()
    response = client.label_detection(
        image=vision.Image(content=payload["image_bytes"]),
        max_results=1,
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    labels = response.label_annotations
    description = labels[0].description if labels else ""
    return {"description": description, "confidence": labels[0].score if labels else 0.0, "max_labels": cfg.max_labels}
