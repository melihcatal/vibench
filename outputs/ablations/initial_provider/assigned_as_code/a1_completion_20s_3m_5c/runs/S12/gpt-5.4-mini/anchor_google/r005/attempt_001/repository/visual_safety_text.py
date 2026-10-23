from google.cloud import vision

from vision_client import get_google_vision_client


def visual_safety_text(payload, config=None):
    client = get_google_vision_client()
    response = client.safe_search_detection(image=vision.Image(content=payload["image_bytes"]))
    if response.error.message:
        raise RuntimeError(response.error.message)
    return {"unsafe_text": any(v in (2, 3, 4) for v in [int(response.safe_search_annotation.adult), int(response.safe_search_annotation.violence), int(response.safe_search_annotation.racy)])}
