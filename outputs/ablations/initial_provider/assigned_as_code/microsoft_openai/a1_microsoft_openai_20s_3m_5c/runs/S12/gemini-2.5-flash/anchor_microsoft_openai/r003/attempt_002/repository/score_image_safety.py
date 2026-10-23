from google.cloud import vision
from vision_client import get_vision_client

def score_image_safety(image_bytes: bytes, config: dict = None) -> dict:
    client = get_vision_client()
    image = vision.Image(content=image_bytes)

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    safety_scores = {
        "adult": safe_search.adult.name,
        "spoof": safe_search.spoof.name,
        "medical": safe_search.medical.name,
        "violence": safe_search.violence.name,
        "racy": safe_search.racy.name,
    }

    return {"safety_scores": safety_scores}
