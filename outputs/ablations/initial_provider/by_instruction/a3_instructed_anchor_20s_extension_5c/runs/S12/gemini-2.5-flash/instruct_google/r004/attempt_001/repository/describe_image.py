from vision_client import get_vision_client
from google.cloud import vision

def describe_image(image_content: bytes) -> str:
    client = get_vision_client()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    descriptions = [label.description for label in response.label_annotations if label.score > 0.7]

    if descriptions:
        return "An image depicting: " + ", ".join(descriptions[:5]) + "."
    else:
        return "No clear description available for the image."
