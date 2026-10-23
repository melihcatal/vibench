from google.cloud import vision

from vision_client import build_image, get_vision_client
from vision_models import normalize_safe_search


def score_image_safety(payload, config=None):
    client = get_vision_client()
    response = client.safe_search_detection(image=build_image(payload))
    if response.error.message:
        raise RuntimeError(response.error.message)
    safe = normalize_safe_search(response.safe_search_annotation)
    return {"safety": safe}
