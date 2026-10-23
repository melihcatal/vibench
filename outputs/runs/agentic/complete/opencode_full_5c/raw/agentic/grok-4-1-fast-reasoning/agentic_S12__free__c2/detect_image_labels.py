from google.cloud import vision
import vision_client


def detect_image_labels(image_path: str) -> list[str]:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=vision_client.get_image_bytes(image_path))
    response = client.label_detection(image=image, max_results=10)
    labels = [label.description for label in response.label_annotations]
    return labels
