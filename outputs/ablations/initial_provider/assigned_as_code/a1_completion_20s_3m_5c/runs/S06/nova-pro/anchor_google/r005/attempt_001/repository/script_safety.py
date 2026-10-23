from google.cloud import vision


def check_safety(text):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(content=text.encode('utf-8'))
    if response.error.message:
        raise Exception(response.error.message)
    return response.text_annotations[0].description
