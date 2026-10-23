from google.cloud import vision

def get_vision_client():
    """
    Returns a Google Cloud Vision client.
    """
    return vision.ImageAnnotatorClient()

def get_document_text_detection_client():
    """
    Returns a Google Cloud Vision client specifically for document text detection.
    """
    return vision.ImageAnnotatorClient()
