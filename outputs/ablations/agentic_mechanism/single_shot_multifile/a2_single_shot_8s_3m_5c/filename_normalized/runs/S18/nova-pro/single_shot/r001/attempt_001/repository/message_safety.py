from google.cloud import vision_v1

def check_text_safety(text):
    client = vision_v1.ImageAnnotatorClient()
    document = vision_v1.Image(content=text.encode('utf-8'))
    response = client.text_detection(document)
    for annotation in response.text_annotations:
        if 'unsafe' in annotation.description.lower():
            return False
    return True