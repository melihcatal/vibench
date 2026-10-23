from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import create_vision_image, parse_label_detection_response


def describe_image(image_path_or_bytes):
    """
    Generates a short visual description for an image using Google Cloud Vision AI.
    Provider: Google Cloud Vision AI
    """
    client = get_vision_client()
    image = create_vision_image(image_path_or_bytes)

    response = client.label_detection(image=image)
    labels = parse_label_detection_response(response)

    if labels:
        return "The image likely contains: " + ", ".join(labels) + "."
    return "No clear description could be generated for the image."
