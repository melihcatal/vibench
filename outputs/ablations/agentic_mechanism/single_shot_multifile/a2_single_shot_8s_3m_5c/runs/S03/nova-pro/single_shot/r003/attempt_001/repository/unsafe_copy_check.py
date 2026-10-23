import os
from google.cloud import vision

def get_vision_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    return vision.ImageAnnotatorClient()

def check_unsafe_copy(text):
    client = get_vision_client()
    # Placeholder for actual unsafe content check logic
    return 'Unsafe content check based on Google Cloud Vision API'
