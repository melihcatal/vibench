from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageInput, ImageDescription
import base64

def describe_image(image_input: ImageInput) -> ImageDescription:
    """Generates a short visual description for an image using Google Cloud Vision labels."""
    client = get_vision_client()
    image = vision.Image(content=base64.b64decode(image_input.image_content_base64))

    # Using label detection as a simple form of description generation.
    response = client.label_detection(image=image, max_results=5)
    descriptions = [label.description for label in response.label_annotations if label.score > 0.7]
    
    if descriptions:
        description_text = "An image depicting " + ", ".join(descriptions) + "."
    else:
        description_text = "Could not generate a clear description for the image."

    return ImageDescription(description=description_text)
