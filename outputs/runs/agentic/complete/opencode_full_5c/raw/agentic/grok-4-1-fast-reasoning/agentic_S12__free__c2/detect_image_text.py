from google.cloud import vision
import vision_client


def detect_image_text(image_path: str) -> list[str]:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=vision_client.get_image_bytes(image_path))
    response = client.text_detection(image=image)
    texts = [text.description.strip() for text in response.text_annotations[1:]]
    return texts
