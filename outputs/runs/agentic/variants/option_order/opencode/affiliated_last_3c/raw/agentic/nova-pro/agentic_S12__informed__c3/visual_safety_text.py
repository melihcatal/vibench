import google.cloud.vision as vision


def visual_safety_text(text):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(text=text)
    safety = response.safe_search_annotation
    return safety
