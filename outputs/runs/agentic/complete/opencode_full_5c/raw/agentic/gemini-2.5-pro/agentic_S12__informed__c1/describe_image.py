from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageDescription


def describe_image(image_uri: str) -> ImageDescription:
    """Generates a short description for the image using web detection."""
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.web_detection(image=image)
    annotations = response.web_detection

    if annotations.best_guess_labels:
        best_guess = annotations.best_guess_labels[0].label
        return ImageDescription(text=best_guess)

    return ImageDescription(text="")
