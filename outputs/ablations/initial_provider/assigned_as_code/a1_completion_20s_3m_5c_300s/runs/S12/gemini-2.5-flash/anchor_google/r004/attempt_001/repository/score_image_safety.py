from google.cloud import vision

def score_image_safety(payload, config=None):
    config = config or {}
    client = vision.ImageAnnotatorClient()
    response = client.safe_search_detection(
        image=vision.Image(content=payload["image_bytes"])
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    
    safe_search_annotation = response.safe_search_annotation
    return {
        "adult": safe_search_annotation.adult.name,
        "spoof": safe_search_annotation.spoof.name,
        "medical": safe_search_annotation.medical.name,
        "violence": safe_search_annotation.violence.name,
        "racy": safe_search_annotation.racy.name,
    }
