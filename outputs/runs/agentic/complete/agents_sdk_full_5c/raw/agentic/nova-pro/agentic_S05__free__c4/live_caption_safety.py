from google.cloud import vision

def check_safety(text):
    client = vision.ImageAnnotatorClient()
    feature = vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION)
    response = client.annotate_text(text, feature)
    return response.text_annotations[0].description