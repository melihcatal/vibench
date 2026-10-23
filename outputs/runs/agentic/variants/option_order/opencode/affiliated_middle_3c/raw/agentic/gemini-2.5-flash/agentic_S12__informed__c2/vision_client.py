from google.cloud import vision_v1


def get_vision_client():
    """Initializes and returns a Google Cloud Vision client."""
    return vision_v1.ImageAnnotatorClient()
