from google.cloud import vision

def get_vision_client():
    return vision.ImageAnnotatorClient()

def normalize_response(response):
    return response.__dict__