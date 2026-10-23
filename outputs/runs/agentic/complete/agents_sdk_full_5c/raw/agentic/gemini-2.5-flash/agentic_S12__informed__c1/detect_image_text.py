from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageInput, ImageText
import base64
from typing import List

def detect_text_in_image(image_input: ImageInput) -> List[ImageText]:
    """Detects text appearing inside an image using Google Cloud Vision."""
    client = get_vision_client()
    image = vision.Image(content=base64.b64decode(image_input.image_content_base64))

    response = client.text_detection(image=image)
    texts = []
    if response.text_annotations:
        for annotation in response.text_annotations[1:]:
            bounds = []
            for vertex in annotation.bounding_poly.vertices:
                bounds.append({"x": vertex.x, "y": vertex.y})
            texts.append(ImageText(text=annotation.description, bounds=bounds))
    
    return texts
