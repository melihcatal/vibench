import os
from google.cloud import vision_v1
from vision_client import get_vision_client, create_vision_image_object
from vision_models import ImageData, TextResult

def detect_image_text(image_data: ImageData) -> list[TextResult]:
    """
    Detects text appearing inside an image using Google Cloud Vision AI.
    """
    client = get_vision_client()
    image = create_vision_image_object(image_data)

    features = [vision_v1.Feature(type_=vision_v1.Feature.Type.TEXT_DETECTION)]
    request = vision_v1.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request)

    texts = []
    if response.text_annotations:
        for text in response.text_annotations:
            vertices = [{'x': v.x, 'y': v.y} for v in text.bounding_poly.vertices]
            texts.append(TextResult(description=text.description, bounding_poly=vertices))
    return texts
