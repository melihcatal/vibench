from google.cloud import vision

def check_unsafe_content(text):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(content=text)
    if response.error.message:
        raise Exception(response.error.message)
    for annotation in response.text_annotations:
        if annotation.description in ['adult', 'violence', 'medical']:
            return True
    return False