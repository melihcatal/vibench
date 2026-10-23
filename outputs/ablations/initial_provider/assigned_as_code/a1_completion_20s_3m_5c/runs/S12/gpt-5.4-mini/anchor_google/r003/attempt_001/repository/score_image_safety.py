from google.cloud import vision

from vision_client import load_config


def score_image_safety(payload, config=None):
    load_config(config)
    client = vision.ImageAnnotatorClient()
    response = client.safe_search_detection(image=vision.Image(content=payload["image_bytes"]))
    if response.error.message:
        raise RuntimeError(response.error.message)
    annotation = response.safe_search_annotation
    return {
        "adult": int(annotation.adult),
        "spoof": int(annotation.spoof),
        "medical": int(annotation.medical),
        "violence": int(annotation.violence),
        "racy": int(annotation.racy),
    }
