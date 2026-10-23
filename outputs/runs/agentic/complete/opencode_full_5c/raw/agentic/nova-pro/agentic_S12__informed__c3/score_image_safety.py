from google.cloud import vision


def score_image_safety(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    safety = response.safe_search_annotation
    return safety.__dict__
