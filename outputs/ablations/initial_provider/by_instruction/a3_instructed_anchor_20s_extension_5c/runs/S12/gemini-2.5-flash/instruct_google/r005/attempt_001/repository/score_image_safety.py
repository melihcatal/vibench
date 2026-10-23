from vision_client import get_vision_client
from vision_models import create_image_from_bytes, create_feature
from google.cloud import vision
from typing import Dict, Any

def score_image_safety(image_content: bytes) -> Dict[str, Any]:
    client = get_vision_client()
    image = create_image_from_bytes(image_content)
    feature = create_feature(vision.Feature.Type.SAFE_SEARCH_DETECTION)
    response = client.annotate_image(request={'image': image, 'features': [feature]})
    safe_search_annotation = response.safe_search_annotation

    safety_scores = {
        "adult": safe_search_annotation.adult.name,  # UNKNOWN, VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY
        "spoof": safe_search_annotation.spoof.name,
        "medical": safe_search_annotation.medical.name,
        "violence": safe_search_annotation.violence.name,
        "racy": safe_search_annotation.racy.name,
    }
    return safety_scores
