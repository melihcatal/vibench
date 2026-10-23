from google.cloud import vision

def check_safety(text):
    client = vision.ImageAnnotatorClient()

    response = client.text_detection(image=None, content=text)

    if response.error.message:
        raise Exception(
            '{}
'.format(response.error.message))

    for annotation in response.text_annotations:
        if annotation.description in ['violence', 'gore', 'sexual']:
            return False
    return True