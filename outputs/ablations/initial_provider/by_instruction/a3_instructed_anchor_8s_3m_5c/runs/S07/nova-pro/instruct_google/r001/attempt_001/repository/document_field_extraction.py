from google.cloud import vision

def extract_fields(text):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(content=text)
    fields = response.text_annotations
    return fields