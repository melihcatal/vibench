from google.cloud import vision

def score_image_safety(image_path):
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())

    response = client.safe_search_detection(image=image)

    if response.error.message:
        raise Exception(response.error.message)

    safety_labels = response.safe_search_annotation
    return safety_labels

