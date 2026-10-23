import os
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def extract_key_values(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    key_values = {}
    for page in response.pages:
        for element in page.blocks:
            if element.HasField('key_value'):
                key_values[element.key_value.key] = element.key_value.value
    return key_values