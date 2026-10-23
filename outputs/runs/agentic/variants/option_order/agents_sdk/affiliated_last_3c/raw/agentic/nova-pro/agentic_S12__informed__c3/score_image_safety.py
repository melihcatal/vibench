import os
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

client = vision.ImageAnnotatorClient()

def score_safety(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.safe_search_detection(image=image)
        safety = response.safe_search_annotation
        print('Safety:')
        print(f'Adult: {safety.adult}')
        print(f'Medical: {safety.medical}')
        print(f'Violence: {safety.violence}')