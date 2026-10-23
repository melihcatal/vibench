from google.cloud import vision

def get_vision_client():
    """
    Provides a Google Cloud Vision API client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication.
    """
    return vision.ImageAnnotatorClient()
