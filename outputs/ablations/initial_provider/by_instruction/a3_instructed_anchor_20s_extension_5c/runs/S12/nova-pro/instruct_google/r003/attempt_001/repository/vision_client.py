from google.cloud import vision

def get_vision_client():
    return vision.ImageAnnotatorClient()