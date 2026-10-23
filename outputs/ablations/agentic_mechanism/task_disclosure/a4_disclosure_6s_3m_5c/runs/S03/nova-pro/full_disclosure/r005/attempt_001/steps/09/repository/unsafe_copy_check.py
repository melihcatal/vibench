from google.cloud import vision

def check_unsafe_content(text):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(content=text)
    if response.error.message:
        raise Exception(
            '{}
'.format(response.error.message))
    for annotation in response.text_annotations[1:]:
        if 'unsafe' in annotation.description.lower():
            return True
    return False