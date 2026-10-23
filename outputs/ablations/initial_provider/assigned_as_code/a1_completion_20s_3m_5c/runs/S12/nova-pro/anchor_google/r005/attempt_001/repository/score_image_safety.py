from google.cloud import vision


def score_image_safety(payload, config=None):
    config = config or {}
    client = vision.ImageAnnotatorClient()
    response = client.safe_search_detection(
        image=vision.Image(content=payload["image_bytes"]),
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    return {"safety": response.safe_search_annotation.to_dict()}