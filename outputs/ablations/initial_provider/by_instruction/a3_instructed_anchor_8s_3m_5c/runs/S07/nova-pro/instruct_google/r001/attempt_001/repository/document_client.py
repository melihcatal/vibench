from google.cloud import vision

def get_client():
    return vision.ImageAnnotatorClient()

def normalize_response(response):
    return response.full_text_annotation.text