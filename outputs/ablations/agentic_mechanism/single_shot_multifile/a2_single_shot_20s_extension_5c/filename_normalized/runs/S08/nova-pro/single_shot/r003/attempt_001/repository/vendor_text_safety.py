import os
from google.cloud import vision

def moderate_vendor_text(text):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(content=text.encode('utf-8'))
    if response.error.message:
        raise Exception(response.error.message)
    for annotation in response.text_annotations:
        if any(keyword in annotation.description for keyword in ['unsafe','sensitive']):
            return 'Text contains sensitive content'
    return 'Text is safe'