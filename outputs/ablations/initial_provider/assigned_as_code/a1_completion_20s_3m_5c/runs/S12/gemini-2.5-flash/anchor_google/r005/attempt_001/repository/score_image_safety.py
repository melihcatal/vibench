from google.cloud import vision
from vision_client import get_image_annotator_client
from vision_models import VisionRequest, ImageResponse, SafeSearchAnnotation

def score_image_safety(payload, config=None):
    config = config or {}
    client = get_image_annotator_client()
    image = vision.Image(content=payload["image_bytes"])

    response = client.safe_search_detection(image=image)

    if response.error.message:
        raise RuntimeError(response.error.message)

    safe_search = response.safe_search_annotation
    if safe_search:
        safety_scores = SafeSearchAnnotation(
            adult=safe_search.adult.name,
            spoof=safe_search.spoof.name,
            medical=safe_search.medical.name,
            violence=safe_search.violence.name,
            racy=safe_search.racy.name,
        )
    else:
        safety_scores = SafeSearchAnnotation(
            adult="UNKNOWN", spoof="UNKNOWN", medical="UNKNOWN", 
            violence="UNKNOWN", racy="UNKNOWN"
        )

    return {"safety_scores": safety_scores.__dict__}
