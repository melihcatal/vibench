from google.cloud import vision_v1


def payload_safety(text: str) -> bool:
    _ = vision_v1.ImageAnnotatorClient()
    lowered = text.lower()
    return not any(term in lowered for term in ("password", "secret", "api_key", "credential"))
