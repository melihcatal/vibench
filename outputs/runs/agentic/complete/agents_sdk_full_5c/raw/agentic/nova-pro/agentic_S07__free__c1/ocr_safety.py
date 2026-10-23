import os
import google.auth
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
client = vision.ImageAnnotatorClient()

def check_safety(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    return response.safe_search_annotation