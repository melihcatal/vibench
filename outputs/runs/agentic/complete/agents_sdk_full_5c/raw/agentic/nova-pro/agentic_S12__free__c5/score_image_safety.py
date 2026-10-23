from google.cloud import vision

def score_safety(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    response = client.safe_search_detection(image=image)
    safety = response.safe_search_annotation
    print('Safety:', safety)