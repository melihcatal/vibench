from google.cloud import vision
from vision_models import ImageLabels, parse_labels

def detect_image_labels(image_path: str) -> ImageLabels:
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return parse_labels(labels)