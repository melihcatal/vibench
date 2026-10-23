from vision_client import get_vision_client
from google.cloud import vision
from typing import Dict, Any

def score_image_safety(image_content: bytes) -> Dict[str, Any]:
    client = get_vision_client()
    image = vision.Image(content=image_content)

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    safety_scores = {
        'adult': vision.Likelihood(safe_search.adult).name,
        'spoof': vision.Likelihood(safe_search.spoof).name,
        'medical': vision.Likelihood(safe_search.medical).name,
        'violence': vision.Likelihood(safe_search.violence).name,
        'racy': vision.Likelihood(safe_search.racy).name,
    }
    return safety_scores
