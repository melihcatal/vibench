from google.cloud import vision


def get_vision_client():
    """Returns a Google Cloud Vision AI client."""
    return vision.ImageAnnotatorClient()
