import os
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def extract_tables(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    tables = []
    for page in response.pages:
        for table in page.tables:
            tables.append(table)
    return tables