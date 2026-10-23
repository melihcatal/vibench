from google.cloud import vision
from vision_models import ImageSafety, parse_safety_annotation

def score_image_safety(image_path: str) -> ImageSafety:
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    safety_annotation = response.safe_search_annotation
    return parse_safety_annotation(safety_annotation)