from google.cloud import vision

def score_image_safety(payload, config=None):
    config = config or {}
    client = vision.ImageAnnotatorClient()
    response = client.safe_search_detection(
        image=vision.Image(content=payload["image_bytes"]),
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    return {
        "adult": response.safe_search_annotation.adult,
        "spoof": response.safe_search_annotation.spoof,
        "medical": response.safe_search_annotation.medical,
        "violence": response.safe_search_annotation.violence,
        "racy": response.safe_search_annotation.racy,
    }