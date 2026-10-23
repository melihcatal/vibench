import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

client = vision_v1.ImageAnnotatorClient()

def check_safety(text):
    document = types.Image(content=text)
    response = client.text_detection(image=document)
    for annotation in response.text_annotations:
        if 'unsafe' in annotation.description.lower():
            return True
    return False