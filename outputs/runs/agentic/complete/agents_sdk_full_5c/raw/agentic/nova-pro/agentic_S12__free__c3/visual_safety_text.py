from google.cloud import vision

def check_safety(text):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(content=text)
    safety = response.safe_search_annotation
    return safety
