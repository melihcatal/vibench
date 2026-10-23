import io
from google.cloud import vision
from vision_client import load_image_bytes


def detect_image_text(image_path: str) -> list[str]:
    client = vision.ImageAnnotatorClient()
    content = load_image_bytes(image_path)
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = [annotation.description for annotation in response.text_annotations[1:]]
    return texts
