from google.cloud import vision
from google.cloud.vision import types


def score_image_safety(payload, config=None):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=payload['image_bytes'])
    response = client.safe_search_detection(image=image)
    safety = response.safe_search_annotation
    return {'safety': {'adult': safety.adult, 'spoof': safety.spoof, 'medical': safety.medical, 'violence': safety.violence}}