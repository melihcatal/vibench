import os
from google.cloud import vision

def check_unsafe_content(text):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(content=text)
    if response.error.message:
        raise Exception(
            '{}
'.format(response.error.message))
    for annotation in response.text_annotations:
        if 'unsafe' in annotation.description.lower():
            return True
    return False