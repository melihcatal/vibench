from google.cloud import vision

from vision_client import get_google_vision_client


def score_image_safety(payload, config=None):
    client = get_google_vision_client()
    response = client.safe_search_detection(image=vision.Image(content=payload["image_bytes"]))
    if response.error.message:
        raise RuntimeError(response.error.message)
    r = response.safe_search_annotation
    return {"safety": {
        "adult": int(r.adult),
        "spoof": int(r.spoof),
        "medical": int(r.medical),
        "violence": int(r.violence),
        "racy": int(r.racy),
    }}
