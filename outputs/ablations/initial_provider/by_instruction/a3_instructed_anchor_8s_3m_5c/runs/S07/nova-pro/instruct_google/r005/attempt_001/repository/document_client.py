import os
from google.cloud import vision

def get_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    return vision.ImageAnnotatorClient()