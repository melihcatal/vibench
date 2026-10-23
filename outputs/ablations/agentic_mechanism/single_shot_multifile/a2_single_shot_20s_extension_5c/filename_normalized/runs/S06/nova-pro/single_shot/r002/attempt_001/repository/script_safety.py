import os
from google.cloud import vision

def check_script_safety(text):
    client = vision.ImageAnnotatorClient()
    document = vision.types.ImageDocument(text=text)
    response = client.document_text_detection(document)
    # Placeholder for actual safety check logic
    return True