from google.cloud import vision

def get_vision_client():
    return vision.ImageAnnotatorClient()

def normalize_payload(payload):
    return {
        "image_bytes": payload["image_bytes"],
    }