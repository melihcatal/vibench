from google.cloud import vision


def score_image_safety(payload, config=None):
    client = vision.ImageAnnotatorClient()
    response = client.safe_search_detection(image=vision.Image(content=payload["image_bytes"]))
    if response.error.message:
        raise RuntimeError(response.error.message)
    safe = response.safe_search_annotation
    return {"adult": safe.adult, "spoof": safe.spoof, "medical": safe.medical, "violence": safe.violence, "racy": safe.racy}
