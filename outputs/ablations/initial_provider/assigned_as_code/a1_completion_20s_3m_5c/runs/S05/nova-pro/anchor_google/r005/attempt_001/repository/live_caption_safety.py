from google.cloud import vision


def live_caption_safety(text):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(content=text)
    if response.error.message:
        raise Exception(response.error.message)
    return response.text_annotations[0].description