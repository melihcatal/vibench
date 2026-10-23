import os
from google.cloud import vision

def moderate_transcript(text):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(content=text)
    if response.error.message:
        raise Exception(response.error.message)
    return text